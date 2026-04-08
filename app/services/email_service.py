import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

def send_email(receiver_email, otp):
    sender_email =os.getenv("Sender_Email")
    sender_password =os.getenv("App_Password")
    APP_NAME = "SecureAuth" 
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{APP_NAME} - Your Verification Code"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    html = f"""
<html>
<head>
<meta charset="UTF-8">
<title>Student System Verification</title>
</head>

<body style="margin:0; padding:0; background-color:#eef2f7; font-family:Arial, sans-serif;">

<table align="center" width="100%" cellpadding="0" cellspacing="0" style="padding:20px 0;">
<tr>
<td align="center">

<!-- Main Container -->
<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 6px 20px rgba(0,0,0,0.08);">

    <!-- Header -->
    <tr>
        <td style="background:linear-gradient(135deg,#198754,#20c997); padding:20px; text-align:center; color:#ffffff; font-size:20px; font-weight:bold;">
            🎓 Student Performance Prediction System
        </td>
    </tr>

    <!-- Body -->
    <tr>
        <td style="padding:30px; color:#333333;">

            <h2 style="margin-top:0;">🔐 Email Verification</h2>

            <p style="font-size:15px; line-height:1.6;">
                Hello,
                <br><br>
                Welcome to the <b>Student Performance Prediction System</b>.
                Verify your email using the OTP below to access your performance insights.
            </p>

            <!-- OTP Box -->
            <div style="text-align:center; margin:30px 0;">
                <span style="
                    display:inline-block;
                    padding:15px 35px;
                    font-size:30px;
                    letter-spacing:8px;
                    font-weight:bold;
                    background:#e6fcf5;
                    color:#198754;
                    border-radius:12px;
                    border:2px dashed #20c997;">
                    {otp}
                </span>
            </div>

            <p style="font-size:14px; color:#555;">
                ⏳ This OTP is valid for <b>2 minutes</b>.
            </p>

            <p style="font-size:14px; color:#999;">
                If you did not request this verification, you can safely ignore this email.
            </p>

            <p style="margin-top:30px;">
                Regards,<br>
                <b>SPPS Team</b><br>
            </p>

        </td>
    </tr>

    <!-- Footer -->
    <tr>
        <td style="background:#f1f3f5; padding:15px; text-align:center; font-size:12px; color:#888;">
            © 2026 Student Performance Prediction System <br>
            AI-Based Academic Analytics Platform
        </td>
    </tr>

</table>

</td>
</tr>
</table>

</body>
</html>"""

    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    finally:
        server.quit()
    
