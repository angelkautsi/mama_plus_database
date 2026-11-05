from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Date,
    ForeignKey, CheckConstraint, Text
)
from sqlalchemy.sql import func

from database.database import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
    CheckConstraint(
        "role IN ('patient', 'nurse', 'admin')",
        name="check_user_role"
    ),
)

    user_id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, nullable=False, index=True)

    email = Column(String(100), unique=True, nullable=False, index=True)

    password_hash = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        unique=True,
        nullable=False
    )

    date_of_birth = Column(Date, nullable=True)

    phone_number = Column(String(20), nullable=True)

    address = Column(String(255), nullable=True)

    emergency_contact_name = Column(String(100), nullable=True)

    emergency_contact_phone = Column(String(20), nullable=True)

class Nurse(Base):
    __tablename__ = "nurses"

    nurse_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        unique=True,
        nullable=False
    )

    facility_id = Column(
        Integer,
        ForeignKey("facilities.facility_id"),
        nullable=True
    )

    professional_registration_number = Column(
        String(100),
        unique=True,
        nullable=True
    )

    phone_number = Column(String(20), nullable=True)

    specialization = Column(String(100), nullable=True)

class Facility(Base):
    __tablename__ = "facilities"

    facility_id = Column(Integer, primary_key=True, index=True)

    facility_name = Column(String(150), nullable=False)

    facility_type = Column(String(50), nullable=True)

    address = Column(String(255), nullable=True)

    district = Column(String(100), nullable=True)

    phone_number = Column(String(20), nullable=True)

    email = Column(String(100), nullable=True)

class ITPersonnel(Base):
    __tablename__ = "it_personnel"

    it_personnel_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        unique=True,
        nullable=False
    )

    employee_number = Column(
        String(50),
        unique=True,
        nullable=True
    )

    phone_number = Column(String(20), nullable=True)

    department = Column(String(100), nullable=True)

class Pregnancy(Base):
    __tablename__ = "pregnancies"

    pregnancy_id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.patient_id"),
        nullable=False
    )

    last_menstrual_period = Column(Date, nullable=True)

    expected_delivery_date = Column(Date, nullable=True)

    pregnancy_start_date = Column(Date, nullable=True)

    pregnancy_status = Column(String(30), default="active")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SymptomLog(Base):
    __tablename__ = "symptom_logs"

    symptom_log_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.patient_id"),
        nullable=False
    )

    pregnancy_id = Column(
        Integer,
        ForeignKey("pregnancies.pregnancy_id"),
        nullable=False
    )

    symptoms = Column(String(500), nullable=False)

    severity = Column(String(30), nullable=True)

    notes = Column(String(1000), nullable=True)

    recorded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.patient_id"),
        nullable=False
    )

    nurse_id = Column(
        Integer,
        ForeignKey("nurses.nurse_id"),
        nullable=False
    )

    facility_id = Column(
        Integer,
        ForeignKey("facilities.facility_id"),
        nullable=False
    )

    appointment_date = Column(DateTime, nullable=False)

    purpose = Column(String(255), nullable=True)

    status = Column(String(30), default="scheduled")

    notes = Column(String(1000), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)

    sender_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    receiver_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    message_content = Column(String(2000), nullable=False)

    sent_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    is_read = Column(Boolean, default=False, nullable=False)

class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    title = Column(String(150), nullable=False)

    message = Column(String(500), nullable=False)

    notification_type = Column(String(50), nullable=True)

    is_read = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"

    article_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(String(255), nullable=False)

    content = Column(Text, nullable=False)

    category = Column(String(100), nullable=True)

    source_name = Column(String(255), nullable=True)

    source_url = Column(String(500), nullable=True)

    reviewed_by = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=True
    )

    is_approved = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class ChatbotConversation(Base):
    __tablename__ = "chatbot_conversations"

    conversation_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    is_active = Column(Boolean, default=True, nullable=False)

class ChatbotMessage(Base):
    __tablename__ = "chatbot_messages"

    chatbot_message_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    conversation_id = Column(
        Integer,
        ForeignKey("chatbot_conversations.conversation_id"),
        nullable=False
    )

    sender = Column(String(20), nullable=False)

    message_content = Column(String(5000), nullable=False)

    sent_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class ChatbotFeedback(Base):
    __tablename__ = "chatbot_feedback"

    feedback_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    chatbot_message_id = Column(
        Integer,
        ForeignKey("chatbot_messages.chatbot_message_id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    rating = Column(Integer, nullable=False)

    comments = Column(String(1000), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )