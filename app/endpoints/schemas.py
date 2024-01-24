from ninja import Schema, Field
from typing import Optional, Union


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
    kind_id: str = Field(None, alias="KindId")


class Patient(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    name: str = None
    sex: str
    birth_date: str = Field(None, alias="birthDate")
    chip: str = None
    brand: str = None
    photo: str = None
    card_number: str = Field(None, alias="cardNumber")
    breed_enote_id: str = Field(alias="breedEnoteId")
    kind_enote_id: str = Field(alias="kindEnoteId")
    client_enote_id: str = Field(alias="clientEnoteId")
    is_approximate_birth_date: bool = Field(None, alias="isApproximateBirthDate")
    is_castrated: bool = Field(None, alias="isCastrated")
    time_of_death: Union[str, None] = Field(None, alias="timeOfDeath")
    attributes: Union[list[dict], None] = None


class Client(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    is_confirmed: bool = Field(False, alias="isConfirmed")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    last_name: str = Field(alias="lastName")
    contact_information: list[ContactInformation] = None
    attributes: Union[list[dict], None] = None


class DiscountCard(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(alias="objectState")
    name: str = None
    client_enote_id: str = Field(None, alias="clientEnoteId")
    card_number: str = Field(None, alias="codeCard")
    category_enote_id: str = Field(None, alias="categoryOfDiscountEnoteId")
    validity_date: str = Field(None, alias="validityDate")
    description: str = Field(None, alias="cardDescription")


class DiscountCardCategory(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(alias="objectState")
    name: str = None


class Specialization(Schema):
    enote_id: str = Field(None, alias="enoteId")
    title: str = None


class DoctorAttribute(Schema):
    type: str = None
    title: str = None
    presentation: str = None
    value: str = None


class Doctor(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(None, alias="middleName")
    last_name: str = Field(alias="lastName")
    specialization: Union[list[Specialization], str]
    position: str = None
    rank: str = Field(None, alias="scientificRank")
    photo_url: str = Field(None, alias="photoUrl")
    fired_date: Union[str, None] = Field(None, alias="layoffDate")
    attributes: Union[list[DoctorAttribute], None] = None


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
    date: str = Field(None, alias="appointmentDate")
    new_client: bool = Field(None, alias="newClient")
    direct_visit: bool = Field(None, alias="directVisit")
    type: str = Field(None, alias="appointmentType")
    status: str = Field(None, alias="appointmentStatus")
    awaiting_confirmation: bool = Field(None, alias="awaitingConfirmation")
    department_enote_id: str = Field(alias="departmentEnoteId")
    doctor_enote_id: Union[str, None] = Field(None, alias="doctorEnoteId")
    visit_kind_id: str = Field(alias="visitKindId")
    service: Union[AppointmentService, None] = None
    client_enote_id: Union[str, None] = Field(alias="clientEnoteId")
    patient_enote_id: Union[str, None] = Field(alias="patientEnoteId")
    client_info: Union[AppointmentClientInfo, None] = Field(
        None, alias="clientInformation"
    )
    description: str = Field(None, alias="appointmentDescription")
    start_time: str = Field(None, alias="startTime")
    end_time: str = Field(None, alias="endTime")


class Weighing(Schema):
    enote_id: str = Field(alias="enoteId")
    state: str = Field(None, alias="objectState")
    patient_enote_id: str = Field(alias="patientEnoteId")
    weight: str = None
    date: str = Field(None, alias="weighingDate")


class Result(Schema):
    enote_id: str = Field(alias="enoteId")
    result: bool
    error_message: str = Field("", alias="errorMessage")

    class Config(Schema.Config):
        populate_by_name = True


class Response(Schema):
    response: list[Result]
