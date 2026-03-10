from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from services.group_request_approval import approve_group_request
from services.reject_group_request import reject_group_request
from services.get_group_request import get_pending_group_requests

from auth.dependencies import get_admin_user
from models.user import User
from schemas.group_requests import RejectGroupRequest

router = APIRouter(
    prefix="/admin/group-requests",
    tags=["Admin Group Requests"]
)

@router.get("/")
def get_group_requests(
        db: Session = Depends(get_db),
        admin: User = Depends(get_admin_user)
):
    try:
        result = get_pending_group_requests(
            db=db,
            current_user=admin
        )

        return {
            "success": True,
            "message": "Pending group requests fetched",
            "data": result
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{request_id}/approve")
def approve_request(
        request_id: int,
        db: Session = Depends(get_db),
        admin: User = Depends(get_admin_user)
):
    try:
        result = approve_group_request(
            db=db,
            group_request_id=request_id,
            current_user=admin
        )

        return {
            "success": True,
            "message": "Group request approved",
            "data": result
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{request_id}/reject")
def reject_request_endpoint(
        request_id: int,
        request: RejectGroupRequest,
        db: Session = Depends(get_db),
        admin: User = Depends(get_admin_user)
):
    try:
        result = reject_group_request(db=db,
                                      group_request_id=request_id,
                                      rejection_reason=request.rejection_reason,
                                      current_user=admin
                                      )
        return {
            "success": True,
            "message": "Group request Rejected",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))