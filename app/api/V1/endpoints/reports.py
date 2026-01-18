from fastapi import Depends,APIRouter
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import csv
import io

from app.db.base import Base
from app.db.session import get_db
from app.models.assets import Asset
from app.models.assignments import Assignment
from app.models.expiry_alerts import ExpiryAlert
from app.models.compliance import Compliance

router = APIRouter()


@router.get("/assets/export")
def export_assets_report(db: Session = Depends(get_db)):
    records = db.query(Asset).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # 🔹 CSV Header (matches Asset model)
    writer.writerow([
        "Asset ID",
        "Name",
        "Category",
        "Serial Number",
        "Brand",
        "Status",
        "Purchase Date",
        "Expiry Date",
        "Warranty Expiry",
        "Notes",
        "Compliance Status",
        "Created At",
        "Updated At"
    ])

    # 🔹 CSV Rows
    for r in records:
        writer.writerow([
            r.assetid,
            r.name,
            r.category,
            r.serialno,
            r.brand,
            r.status,
           # ✅ Date formatting
            r.purchasedate.strftime("%Y-%m-%d") if r.purchasedate else "",
            r.expirydate.strftime("%Y-%m-%d") if r.expirydate else "",
            r.warrentyexpiry.strftime("%Y-%m-%d") if r.warrentyexpiry else "",

            r.notes,
            r.compliance_status,

            r.created_at.strftime("%Y-%m-%d") if r.created_at else "",
            r.updated_at.strftime("%Y-%m-%d") if r.updated_at else ""
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=assets_report.csv"
        }
    )






@router.get("/ownership/export")
def export_assignments_report(db: Session = Depends(get_db)):
    records = db.query(Assignment).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "Assignment ID",
        "Asset ID",
        "Employee ID",
        "Assigned Date",
        "Expected Return Date",
        "Actual Return Date",
        "Assignment Status",
        "Location",
        "Usage Type",
        "Condition At Assign",
        "Approved By",
        "Assigned By",
        "Remarks",
        "Created At",
        "Updated At"
    ])

    for r in records:
        writer.writerow([
            r.assignmentid,
            r.assetid,
            r.employeeid,

            # ✅ Date formatting
            r.assigneddate.strftime("%Y-%m-%d") if r.assigneddate else "",
            r.expectedreturndate.strftime("%Y-%m-%d") if r.expectedreturndate else "",
            r.actualreturndate.strftime("%Y-%m-%d") if r.actualreturndate else "",

            r.assignmentstatus,
            r.location,
            r.usagetype,
            r.conditionatassign,
            r.approvedby,
            r.assignedby,
            r.remarks,

            r.created_at.strftime("%Y-%m-%d") if r.created_at else "",
            r.updated_at.strftime("%Y-%m-%d") if r.updated_at else ""
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=assignments_report.csv"
        }
    )


@router.get("/expiry-compliance/export")
def export_expiry_compliance_csv(db: Session = Depends(get_db)):
    records = (
        db.query(ExpiryAlert, Compliance)
        .join(Compliance, ExpiryAlert.assetid == Compliance.assetid)
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Alert ID",
        "Asset ID",
        "Expiry Date",
        "Days Remaining",
        "Alert Status",
        "Compliance Type",
        "Recommended Action",
        "Compliance Notes",
        "Compliance Created At",
        "Alert Created At"
    ])

    for alert, compliance in records:
        writer.writerow([
            alert.alertid,
            alert.assetid,
            alert.expirydate.strftime("%Y-%m-%d"),
            alert.days_remaining,
            alert.alert_status,
            compliance.complianttype,
            compliance.recommendaction or "",
            compliance.notes or "",
            compliance.created_at.strftime("%Y-%m-%d"),
            alert.created_at.strftime("%Y-%m-%d")
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=expiry_compliance_report.csv"
        }
    )
