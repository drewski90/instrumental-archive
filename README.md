
# Instrumental Archive Platform

Serverless media ingestion and playback platform for managing instrumental audio files.
The system consists of an **AWS SAM infrastructure stack**, a **Flask backend API**, and a **Vue 3 frontend**, providing scalable upload, catalog management, and streaming capabilities.

---

## Architecture Overview

```
Vue 3 Frontend
        ↓
Flask Backend API
        ↓
DynamoDB (Metadata) ←→ S3 Media Bucket (Audio Storage)
        ↓
Lambda Ingestion Handler (S3 Events)
```

Uploads are performed using **pre-signed S3 uploads**, allowing large media files to be transferred directly to S3 without passing through the backend.

---

## Infrastructure (AWS SAM)

The SAM stack provisions:

### DynamoDB Single-Table

* Primary datastore for all application entities
* Composite primary key:

  * `PK` — partition key
  * `SK` — sort key
* Global Secondary Index:

  * `sha256-index` for duplicate detection and object deduplication

### S3 Media Bucket

* Stores uploaded instrumental audio files
* Configured with CORS for direct browser uploads
* Emits **ObjectCreated** and **ObjectRemoved** events

### Media Event Handler (Lambda)

Triggered automatically by S3 object lifecycle events:

* On upload:

  * Registers new object metadata in DynamoDB
* On deletion:

  * Removes associated metadata records

### Programmatic IAM User

Provides application-level access credentials for backend services requiring:

* DynamoDB CRUD operations
* S3 object operations

Access keys are generated as part of the stack outputs for controlled backend integration.

---

## Backend (Flask API)

The backend API provides:

* Authentication-protected endpoints
* Pre-signed upload URL generation
* Media listing with cursor pagination
* Public/private visibility management
* Pre-signed streaming URL generation

Metadata is stored in DynamoDB using a deterministic object-key structure aligned with S3 object paths.

---

## Frontend (Vue 3 + Pinia)

The frontend application enables:

* Instrumental catalog browsing
* Playback queue and streaming player
* Authenticated upload workflows
* Admin visibility toggling
* Automatic Authorization header injection via Axios interceptors

State is managed using Pinia stores for authentication, media catalog pagination, and player control.

---

## Key Design Principles

* Fully serverless ingestion architecture
* Single-table DynamoDB design for flexible entity modeling
* Direct-to-S3 upload pipeline for scalability
* Event-driven metadata registration via Lambda
* Separation of public vs. authenticated media visibility

---
