# Standard Success Responses based on API Docs

MOCK_TEXT2VIDEO_RESPONSE = {
    "code": 0,
    "message": "success",
    "request_id": "req_123456789",
    "data": {
        "task_id": "task_t2v_001",
        "task_info": {"external_task_id": "ext_001"},
        "task_status": "submitted",
        "created_at": 1722769557708,
        "updated_at": 1722769557708
    }
}

MOCK_IMAGE2VIDEO_RESPONSE = {
    "code": 0,
    "message": "success",
    "request_id": "req_987654321",
    "data": {
        "task_id": "task_i2v_002",
        "task_info": {"external_task_id": "ext_002"},
        "task_status": "submitted",
        "created_at": 1722769557709,
        "updated_at": 1722769557709
    }
}

MOCK_TASK_QUERY_SUCCESS = {
    "code": 0,
    "message": "success",
    "request_id": "req_query_001",
    "data": {
        "task_id": "task_t2v_001",
        "task_status": "succeed",
        "task_status_msg": "",
        "task_info": {"external_task_id": "ext_001"},
        "task_result": {
            "videos": [
                {
                    "id": "vid_001",
                    "url": "https://cdn.klingai.com/videos/generated_001.mp4",
                    "duration": "5.0"
                }
            ]
        },
        "created_at": 1722769557708,
        "updated_at": 1722769597708
    }
}

MOCK_IMAGE_GEN_RESPONSE = {
    "code": 0,
    "message": "success",
    "request_id": "req_img_001",
    "data": {
        "task_id": "task_img_001",
        "task_status": "submitted",
        "created_at": 1722769557710,
        "updated_at": 1722769557710,
        "task_result": None
    }
}

MOCK_LIPSYNC_IDENTIFY_RESPONSE = {
    "code": 0,
    "message": "success",
    "request_id": "req_lip_001",
    "data": {
        "session_id": "sess_001",
        "face_data": [
            {
                "face_id": "face_001",
                "face_image": "https://cdn.klingai.com/faces/face_001.jpg",
                "start_time": 0,
                "end_time": 5200
            }
        ]
    }
}

MOCK_ERROR_RESPONSE = {
    "code": 1001,
    "message": "Invalid API Token",
    "request_id": "req_err_001",
    "data": None
}
