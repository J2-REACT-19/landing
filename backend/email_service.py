from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get('GMAIL_USER', ''),
    MAIL_PASSWORD=os.environ.get('GMAIL_PASS', ''),
    MAIL_FROM=os.environ.get('EMAIL_FROM', ''),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fast_mail = FastMail(conf)

async def send_contact_notification(contact_data: dict):
    """
    Send email notification when a new contact form is submitted
    """
    # Create Google Calendar link
    calendar_link = create_google_calendar_link(
        title="Reunión con J2Systems",
        description=f"Reunión agendada con {contact_data['name']} de {contact_data.get('company', 'su empresa')}",
        duration=60  # 60 minutes
    )
    
    # Email HTML template
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">Nuevo Mensaje de Contacto</h1>
            </div>
            
            <div style="background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #1f2937; margin-top: 0;">Detalles del Contacto</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <p style="margin: 10px 0;"><strong>Nombre:</strong> {contact_data['name']}</p>
                    <p style="margin: 10px 0;"><strong>Email:</strong> {contact_data['email']}</p>
                    <p style="margin: 10px 0;"><strong>Empresa:</strong> {contact_data.get('company', 'No especificada')}</p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="color: #1f2937; margin-top: 0;">Mensaje:</h3>
                    <p style="color: #4b5563; line-height: 1.6;">{contact_data['message']}</p>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{calendar_link}" 
                       style="display: inline-block; background: #3b82f6; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                        📅 Agendar Reunión con Google Calendar
                    </a>
                    <p style="color: #6b7280; font-size: 14px; margin-top: 15px;">
                        Haz clic en el botón para agendar una reunión directamente en tu Google Calendar
                    </p>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                    <p style="color: #6b7280; font-size: 12px; text-align: center; margin: 5px 0;">
                        Este mensaje fue enviado desde el formulario de contacto de J2Systems
                    </p>
                    <p style="color: #6b7280; font-size: 12px; text-align: center; margin: 5px 0;">
                        juan@collantes.ec | +593 997 154 016
                    </p>
                </div>
            </div>
        </body>
    </html>
    """
    
    # Create message
    message = MessageSchema(
        subject=f"Nuevo Contacto: {contact_data['name']}",
        recipients=[os.environ.get('EMAIL_FROM')],  # Send to yourself
        body=html,
        subtype="html"
    )
    
    await fast_mail.send_message(message)


def create_google_calendar_link(title: str, description: str, duration: int = 60):
    """
    Create a Google Calendar link for scheduling a meeting
    Args:
        title: Event title
        description: Event description
        duration: Duration in minutes (default 60)
    Returns:
        Google Calendar URL
    """
    import urllib.parse
    
    # URL encode the parameters
    encoded_title = urllib.parse.quote(title)
    encoded_description = urllib.parse.quote(description)
    
    # Create Google Calendar link
    # This opens Google Calendar with pre-filled event details
    calendar_url = (
        f"https://calendar.google.com/calendar/render?"
        f"action=TEMPLATE&"
        f"text={encoded_title}&"
        f"details={encoded_description}&"
        f"duration={duration}"
    )
    
    return calendar_url
