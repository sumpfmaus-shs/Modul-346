import pulumi
import pulumi_aws as aws # Treiber Import

# Create a VPC
vpc = aws.ec2.Vpc("lab-vpc", cidr_block="10.10.0.0/16") # VPC Erstellen (Virtual Private CLoud) (Isuliert die Ressourcen ausschliesslich in desem VPC)

# Create a Subnet
subnet = aws.ec2.Subnet("lab-subnet",	# Typ subnet. ("Subnet Name
    vpc_id=vpc.id,			# Netzwerk ID (Zu identifizierung des Netzwerkes)
    cidr_block="10.10.10.0/24",		# Address Range Definition
    availability_zone="us-east-1a")	# AWS Availability Zone (AWS RZ Standort)

# Create a Security Group #Sicherheitsgruppen definieren
security_group = aws.ec2.SecurityGroup("lab-secgrp", # Die Sicherheitsgruppe lab-secgrp definieren (Lab= Labor sec= Security grp=group der name ist nach best practise prozess gesetzt worden)
    vpc_id=vpc.id,
    description='Enable RDP access', #RDP Access Aktivieren (In Traffic wird der RDP Port aktiviert)
    ingress=[{                  # Ingress = von aussen nach innen (Traffic Direction)
        'protocol': 'tcp',      # Hier wird das Protokoll Definiert
        'from_port': 3389,      # Hier wird der WAN port
        'to_port': 3389,        # Hier wird der to port also ins Netzwerk definiert. Wie man sieht, wird nur ein Portforward gemacht.
        'cidr_blocks': ['0.0.0.0/0'],
    }])

# Function to create an EC2 instance
def create_instance(name, private_ip): # definition der Instanz
    return aws.ec2.Instance(name,
        instance_type="t3.medium",  # 2 Kerne und 4 GB RAM (Die t stufen (Leistungsstufen) sind unter https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html einsehbar)
        vpc_security_group_ids=[security_group.id],
        ami="ami-0069eac59d05ae12b",  # Gültige AMI-ID für Windows Server 2022 in us-west-1 (Sind im Katalob der EC2 Konfiguration einsebar)
        subnet_id=subnet.id,
        private_ip=private_ip,
        tags={
            "Name": name,
        })

# Create EC2 instances (Hier werden die Verschiedenen Instanzen mit Namen und IP Erstellt)
lab_boss1 = create_instance("lab-boss1", "10.10.10.4")
lab_boss2 = create_instance("lab-boss2", "10.10.10.5")
lab_dhcp1 = create_instance("lab-dhcp1", "10.10.10.6")
lab_dhcp2 = create_instance("lab-dhcp2", "10.10.10.7")
lab_file1 = create_instance("lab-file1", "10.10.10.8")
lab_file2 = create_instance("lab-file2", "10.10.10.9")
lab_wsus1 = create_instance("lab-wsus1", "10.10.10.10")

# Export the public IP and DNS of the instances 
pulumi.export('lab_boss1_public_ip', lab_boss1.public_ip)
pulumi.export('lab_boss1_public_dns', lab_boss1.public_dns)
pulumi.export('lab_boss2_public_ip', lab_boss2.public_ip)
pulumi.export('lab_boss2_public_dns', lab_boss2.public_dns)
pulumi.export('lab_dhcp1_public_ip', lab_dhcp1.public_ip)
pulumi.export('lab_dhcp1_public_dns', lab_dhcp1.public_dns)
pulumi.export('lab_dhcp2_public_ip', lab_dhcp2.public_ip)
pulumi.export('lab_dhcp2_public_dns', lab_dhcp2.public_dns)
pulumi.export('lab_file1_public_ip', lab_file1.public_ip)
pulumi.export('lab_file1_public_dns', lab_file1.public_dns)
pulumi.export('lab_file2_public_ip', lab_file2.public_ip)
pulumi.export('lab_file2_public_dns', lab_file2.public_dns)
pulumi.export('lab_wsus1_public_ip', lab_wsus1.public_ip)
pulumi.export('lab_wsus1_public_dns', lab_wsus1.public_dns)
