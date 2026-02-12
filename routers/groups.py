from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.join_group import join_group
from services.list_public_groups import list_public_groups
from services.create_group_request import create_group_request
from services.group_request_approval import approve_group_request
from services.reject_group_request import reject_group_request
from pydantic import BaseModel

router = APIRouter(prefix="/groups",
                   tags=["Groups"])

#Endpoint 1 This is for users trying to join a group
class JoinGroupRequest(BaseModel):
    user_id: int

@router.post("/{group_id}/join")
def join_group_endpoint(
        group_id:int,
        request: JoinGroupRequest,
        db: Session = Depends(get_db)):
        """Join an existing group. User will be charged a prorated price"""
        try:
            result = join_group(db=db,
                                user_id=request.user_id,
                                group_id=group_id)
            return {
                "success": True,
                "message": "Successfully joined group",
                "data": result
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

#Endpoint 2 This is to list out all open available groups
@router.get("/public")
def get_public_groups_endpoint(db:Session = Depends(get_db)):
    """List all public groups available for joining"""
    try:
        groups = list_public_groups(db=db)

        #Return the list with a count
        return {
            "success": True,
            "count": len(groups),
            "groups": groups
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Endpoint 3 This is for users creating group requests
class CreateGroupRequest(BaseModel):
    user_id: int
    subscription_id: int

@router.post("/request")
def create_group_request_endpoint(
        request: CreateGroupRequest,
        db: Session = Depends(get_db)
):
    """Create a new group request"""
    try:
        # Call your service with both user_id and subscription_id
        result = create_group_request(
            db=db,
            user_id = request.user_id,
            subscription_id=request.subscription_id
        )
        return {
            "success": True,
            "message": "Group request created",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint 4
@router.post("/request/{request_id}/approve")
def approve_request_endpoint(
        request_id: int,
        db: Session = Depends(get_db)
):
    """Approve a pending group request and create the group"""
    try:
        group = approve_group_request(
            db=db,
            group_request_id=request_id,
        )
        return {
            "success": True,
            "message": "Group request approved and Group created",
            "data": group
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint 5
class RejectGroupRequest(BaseModel):
    rejection_reason: str
@router.post("/request/{request_id}/reject")
def reject_request_endpoint(
        request_id: int,
        request: RejectGroupRequest,
        db: Session = Depends(get_db)
):
    """Reject a group request"""
    try:
        result = reject_group_request(db=db,
                                      group_request_id=request_id,
                                      rejection_reason=request.rejection_reason
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
