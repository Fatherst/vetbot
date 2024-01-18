from ninja import Schema, Field
from typing import Optional


class ContactInformation(Schema):
    type: str = None
    title: str = None
    value: str = None
    channel: str = None
    authorization: bool = None


class Kind(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    name: str = Field(None)
    kind_id: str = Field(alias="KindId")


class ClientEnote(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    is_confirmed: bool = Field(None, alias="isConfirmed")
    first_name: str = Field("", alias="firstName")
    middle_name: str = Field("", alias="middleName")
    last_name: str = Field("", alias="lastName")
    contact_information: list[ContactInformation] = None
    attributes: Optional[list[dict]] = None


class DiscountCard(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    name: str = None
    client_enote_id: str = Field(None, alias="clientEnoteId")
    card_number: str = Field(None, alias="codeCard")
    category_enote_id: str = Field(None, alias="categoryOfDiscountEnoteId")
    validity_date: str = Field(None, alias="validityDate")
    description: str = Field(None, alias="cardDescription")


class DiscountCardCategory(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    name: str = None


class Specialization(Schema):
    enote_id: str = Field(alias="enoteId")
    title: str


class DoctorAttribute(Schema):
    type: str
    title: str
    presentation: str
    value: str


class Doctor(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    first_name: str = Field("", alias="firstName")
    middle_name: str = Field("", alias="middleName")
    last_name: str = Field("", alias="lastName")
    specialization: list[Specialization]
    position: str = None
    rank: str = Field("", alias="scientificRank")
    photo_url: str = Field("", alias="photoUrl")
    fired_date: Optional[str] = Field(None, alias="layoffDate")
    attributes: list[DoctorAttribute]


class AppointmentService(Schema):
    enote_id: str = Field(alias="enoteId")
    title: str = None
    price: str = None
    description: str = None

class ClientContactInfo(Schema):
    type: str = None
    title: str = None
    value: str = None

class AppointmentClientInfo(Schema):
    client_name: str = Field(alias="clientName")
    patient_name: str = Field(alias="patientName")
    contact_info: list[ClientContactInfo] = Field(alias="contactInformation")


class Appointment(Schema):
    enote_id: str = Field(alias="appointmentEnoteId")
    state: str = Field(None, alias="objectState")
    date: str = Field(alias="appointmentDate")
    new_client: bool = Field(alias="newClient")
    direct_visit: bool = Field(alias="directVisit")
    type: str = Field(alias="appointmentType")
    status: str = Field(alias="appointmentStatus")
    awaiting_confirmation: bool = Field(alias="awaitingConfirmation")
    department_enote_id: str = Field(alias="departmentEnoteId")
    doctor_enote_id: str = Field(alias="doctorEnoteId")
    visit_kind_id: str  = Field(alias="visitKindId")
    service: AppointmentService = None
    client_enote_id: str = Field(alias="clientEnoteId")
    patient_enote_id: str = Field(alias="patientEnoteId")
    client_info: AppointmentClientInfo = Field(alias="clientInformation")
    description: str = Field(alias="appointmentDescription")
    start_time: str = Field(alias="startTime")
    end_time: str = Field(alias="endTime")

class Result(Schema):
    enote_id: str = Field(alias="enoteId")
    result: bool
    error_message: str = Field("", alias="errorMessage")

    class Config(Schema.Config):
        populate_by_name = True


class Response(Schema):
    response: list[Result]
