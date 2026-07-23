#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Email Scanner
# Gwendolyn Dmitruk; 2025
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This program uses Microsoft Outlook CLassic
# Scans inbox for Iridium data files
# Launch by double-clicking on the desktop icon
# or "python3 scanner.py" in Window WSl Ubuntu
# For information on how to disable Windows security prompts
# Visit: https://mariobienaime.com/permanently-disabling-outlook-programmatic-access-security-prompts/
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#Import libraries

import os
import re
import shutil
import time
import win32com.client


# Folder assignments

download_temp = r"C:\Temp\email_downloads"
folder_a = r"Z:\MetData\Base Camp"
folder_b = r"Z:\MetData\Camp 2"

target_ids = {
    "7660": folder_a,
    "3730": folder_b,
}

os.makedirs(download_temp, exist_ok=True)
os.makedirs(folder_a, exist_ok=True)
os.makedirs(folder_b, exist_ok=True)


# outlook configuration

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
shared_mailbox_name = "nvclimatesvc@unr.edu"

recipient = outlook.CreateRecipient(shared_mailbox_name)
recipient.Resolve()
if not recipient.Resolved:
    raise Exception(f"Could not resolve shared mailbox: {shared_mailbox_name}")

inbox = outlook.GetSharedDefaultFolder(recipient, 6)  # 6 = Inbox

def process_emails():
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)

    for message in messages:
        try:
            if message.Class != 43:  # MailItem
                continue

            try:
                sender = message.Sender.GetExchangeUser().PrimarySmtpAddress.lower()
            except:
                sender = message.SenderEmailAddress.lower()

            subject = message.Subject.lower()

            if not (
                sender == 'sbdservice@sbd.iridium.com'
                or (sender == 'gdmitruk@unr.edu' and 'sbd msg from unit' in subject)
                or sender == 'metdata@unr.edu'
            ):
                continue

            attachments = message.Attachments
            processed = False
            unit_id = None

            for i in range(attachments.Count):
                attachment = attachments.Item(i + 1)
                filename = attachment.FileName
                print(f"Attachment found: {filename}")

                match = re.search(r"(\d{15})", filename)
                if not match:
                    print("No 15-digit unit ID in filename, skipping.")
                    continue

                unit_id = match.group(1)
                last4 = unit_id[-4:]

                if last4 not in target_ids:
                    print(f"Unknown unit ID ending in {last4}, skipping.")
                    continue

                if filename.endswith((".txt", ".sbd")):
                    target_folder = target_ids[last4]
                    temp_path = os.path.join(download_temp, filename)
                    attachment.SaveAsFile(temp_path)
                    shutil.move(temp_path, os.path.join(target_folder, filename))
                    processed = True

            if processed and unit_id:
                message.Delete()
                print(f"Processed and deleted email for Unit {unit_id}")

        except Exception as e:
            print(f"Error processing email: {e}")


# === LOOP FOREVER AND EVER AMEN ===

print("Email scanner started... Checking every minute...")
while True:
    process_emails()
    print("Scanning for new data...")
    time.sleep(60)