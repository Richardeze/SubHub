from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.join_group import join_group
from services.list_public_groups import list_public_groups
from services.create_group_request import create_group_request
from schemas.group_requests import CreateGroupRequest
from auth.dependencies import get_current_user
from models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/groups",
                   tags=["Groups"])

@router.post("/{group_id}/join")
def join_group_endpoint(
        group_id:int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
        """Join an existing group. User will be charged a prorated price"""
        try:
            result = join_group(db=db,
                                current_user=current_user,
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
@router.post("/request")
def create_group_request_endpoint(
        request: CreateGroupRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Create a new group request"""
    try:
        result = create_group_request(
            db=db,
            current_user=current_user,
            **request.model_dump()
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


