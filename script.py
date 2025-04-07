import time
import google.auth
import googleapiclient.discovery
from googleapiclient.errors import HttpError

def main():
    # First step, we are defining the variables that will be used during the creation
    PROJECT_ID = "assignment-cloudpart2"
    REGION = "europe-west2"
    ZONE = "europe-west2-a"
    INSTANCE_NAME = "thiago-ubuntu-ca"
    STATIC_IP_NAME = "thiago-net-ca"

    CUSTOM_CPU = 2 #2 vCPUS according to the assignment brief
    CUSTOM_MEMORY_MB = 8192 #8GB RAM
    DISK_SIZE_GB = 250 #250GB for the Storage

    IMAGE_PROJECT = "ubuntu-os-cloud"
    IMAGE_NAME = "ubuntu-2004-focal-v20250313" #Ubuntu 20.04 following the CA requirements

    # Get credentials and build service
    credentials, _ = google.auth.default()
    compute = googleapiclient.discovery.build("compute", "v1", credentials=credentials)

    # In this part we are creating the IP but we also check if it already exists, if so, then we will reuse it.
    # We know this because of the 409 returned, meaning that the IP already exists.
    try:
        compute.addresses().insert(
            project=PROJECT_ID, region=REGION, body={"name": STATIC_IP_NAME}
        ).execute()
    except HttpError as e:
        if e.resp.status != 409:
            print(f"Error creating static IP: {e}")
            return

    time.sleep(2)

    address_resp = compute.addresses().get(
        project=PROJECT_ID, region=REGION, address=STATIC_IP_NAME
    ).execute()
    if "address" not in address_resp:
        print("Could not retrieve the static IP address.")
        return

    external_ip = address_resp["address"]

    # Create firewall rule (HTTP & SSH)
    firewall_body = {
        "name": "allow-http-ssh",
        "network": "global/networks/default",
        "allowed": [{"IPProtocol": "tcp", "ports": ["80", "22"]}],
        "sourceRanges": ["0.0.0.0/0"],
        "targetTags": ["http-server"]
    }
    try:
        compute.firewalls().insert(project=PROJECT_ID, body=firewall_body).execute()
    except HttpError as e:
        if e.resp.status != 409:
            print(f"Error creating firewall rule: {e}")
            return

    # Fetches the Ubuntu Image
    image_resp = compute.images().get(
        project=IMAGE_PROJECT, image=IMAGE_NAME
    ).execute()
    source_disk_image = image_resp["selfLink"]

    # Here we define the machine type, previously defined in the variables
    machine_type = f"zones/{ZONE}/machineTypes/custom-{CUSTOM_CPU}-{CUSTOM_MEMORY_MB}"

    # At this point we create the VM
    instance_body = {
        "name": INSTANCE_NAME,
        "machineType": machine_type,
        "disks": [{
            "boot": True, "autoDelete": True,
            "initializeParams": {
                "diskSizeGb": DISK_SIZE_GB,
                "sourceImage": source_disk_image
            }
        }],
        "networkInterfaces": [{
            "network": "global/networks/default",
            "accessConfigs": [{
                "type": "ONE_TO_ONE_NAT",
                "name": "External NAT",
                "natIP": external_ip
            }]
        }],
        "tags": {"items": ["http-server"]}
    }

    compute.instances().insert(
        project=PROJECT_ID, zone=ZONE, body=instance_body
    ).execute()
    print("Creation request has been sent.")

if __name__ == "__main__":
    main()