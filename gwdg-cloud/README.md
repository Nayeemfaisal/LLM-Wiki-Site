# GWDG Cloud deployment package

This folder is a reproducible deployment package for the **public research wiki**.
It is prepared for a GWDG OpenStack virtual machine but has not been deployed to
GWDG yet. Deployment requires access to the assigned OpenStack project, an SSH
key registered in that project, and a floating IP or approved reverse proxy.

## What this deployment serves

- The public research wiki and dated research outputs.
- The existing public figures and PDF briefings.
- Static content only; no database, API key, student data, or messaging account.

## What must not be copied to the public VM

- Private, unpublished, or licence-restricted raw datasets.
- Student or staff personal data.
- Passwords, OpenStack application credentials, API tokens, SSH private keys, or WhatsApp credentials.
- Any system that impersonates a university communication channel.

## VM setup in GWDG Horizon

1. Log in at `https://cloud.gwdg.de` and select the correct project.
2. Add a personal **public SSH key** under `Compute` / `Key Pairs`.
3. Create an Ubuntu LTS VM. Start with 2 vCPU, 4 GB RAM, and 20 GB disk for the static wiki.
4. Attach a floating IP if the site must be reachable from outside the GWDG network.
5. Create a security group that allows only the chosen public web port. For the default configuration, this is TCP `8080`. Use TCP `80` and `443` only after a domain and TLS plan are approved.
6. Connect by SSH and install Docker using the current Ubuntu/Docker documentation approved for the VM.

## Deploy the public wiki

On the VM, clone the repository and start the static server:

```bash
git clone https://github.com/Nayeemfaisal/LLM-Wiki-Site.git
cd LLM-Wiki-Site/gwdg-cloud
cp .env.example .env
docker compose up -d --build
docker compose ps
```

The site will then be available at `http://<floating-ip>:8080/` when the floating IP and security group are configured.

## Updating the public site

```bash
cd LLM-Wiki-Site
git pull --ff-only
cd gwdg-cloud
docker compose up -d --build
```

## Operational checks

```bash
curl -I http://localhost:8080/
docker compose logs --tail=50 research-wiki
```

## Scope and approval boundary

The public wiki is already available globally through GitHub Pages. The GWDG VM is intended as a controlled research-hosting environment for future reproducible services. Any API, data-processing service, or student/professor messaging prototype needs separate technical, privacy, security, and institutional approval before deployment.
