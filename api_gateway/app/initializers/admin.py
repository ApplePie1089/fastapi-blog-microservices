import logging
import grpc
from api_specs.python_lib.users_pb2 import CreateUserRequest
from api_specs.python_lib.users_pb2_grpc import UsersServiceStub
from api_specs.python_lib.auth_pb2 import UserCreateRequest
from api_specs.python_lib.auth_pb2_grpc import AuthServiceStub
from app.configs.services import USERS_SERVICE, AUTH_SERVICE
from app.configs.admin import ADMIN_EMAIL, ADMIN_PASSWORD


class AdminInitializer:

    def __init__(self):
        self.users_service = UsersServiceStub(grpc.insecure_channel(f"{USERS_SERVICE['host']}:{USERS_SERVICE['port']}"))
        self.auth_service = AuthServiceStub(grpc.insecure_channel(f"{AUTH_SERVICE['host']}:{AUTH_SERVICE['port']}"))

    def create_admin(self):
        logging.info(f"Starting admin initialization for {ADMIN_EMAIL}")

        try:
            user_request = CreateUserRequest(
                email=ADMIN_EMAIL,
                role="USER_ROLE_ADMIN"
            )

            logging.info("Creating user in users_service...")
            user_response = self.users_service.CreateUser(user_request)
            logging.info(f"User created with ID: {user_response.id}")

            auth_request = UserCreateRequest(
                user_id=user_response.id,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD
            )

            logging.info("Creating credentials in auth_service...")
            self.auth_service.CreateUser(auth_request)
            logging.info("Admin initialization completed successfully")

        except grpc.RpcError as e:
            logging.error(f"gRPC Error during admin init: {e.code()} - {e.details()}")
            if e.code() != grpc.StatusCode.ALREADY_EXISTS:
                logging.error("Unexpected gRPC error, but continuing startup...")
        except Exception as e:
            logging.error(f"General error during admin init: {str(e)}")
            logging.error("Admin initialization failed, but continuing startup...")