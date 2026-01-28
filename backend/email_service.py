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
    
    # Email HTML template with inline logo
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <!-- J2Systems Logo SVG -->
                <svg width="180" height="50" viewBox="0 0 240 70" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin: 0 auto 15px;">
                    <defs>
                        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#ffffff;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#e0e7ff;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                    <path d="M 18 12 L 36 3 L 54 12 L 54 30 L 36 39 L 18 30 Z" fill="url(#logoGradient)"/>
                    <text x="36" y="27" font-family="Arial, sans-serif" font-size="19" font-weight="700" fill="#1d4ed8" text-anchor="middle">J2</text>
                    <text x="65" y="30" font-family="Arial, sans-serif" font-size="28" font-weight="600" fill="white" letter-spacing="-0.5">Systems</text>
                    <line x1="65" y1="37" x2="185" y2="37" stroke="white" stroke-width="2.5" opacity="0.3"/>
                </svg>
                <h1 style="color: white; margin: 10px 0 0 0;">Nuevo Mensaje de Contacto</h1>
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
