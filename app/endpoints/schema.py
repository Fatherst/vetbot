from client_auth.models import Client
from ninja import ModelSchema
from .models import Patient, Kind  # , Appointment


class ClientSchema(ModelSchema):
    class Meta:
        model = Client
        fields = [
            "enote_id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "phone_number",
            "tg_chat_id",
        ]


class PatientSchema(ModelSchema):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "birth_date",
            "weight",
            "time_of_death",
            "breed",
            "enote_id",
            "kind",
        ]


class KindSchema(ModelSchema):
    class Meta:
        model = Kind
        fields = ["id", "name", "enote_id"]


# class AppointmentSchema(ModelSchema):
#     class Meta:
#         model = Appointment
#         fields = ['id', 'type', 'enote_id','new_client','status','date','start_time','client','patient'
#                   ,'visit_kind','doctor']
