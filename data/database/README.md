# Granter Database Schema
This document explains the relationships between the main tables used in **Granter**, the AI-powered grant application platform.
---
## Tables and Relationships
### **granter_company**
- Represents a company that applies to funding opportunities.
- **Relations:**
  - Can create **granter_applications** for opportunities.
  - Has associated **granter_companyfiles** for company-related context.
  - Has associated **granter_companymemories** (vectorized text snippets for RAG).
---
### **granter_application**
- An application generated for a specific **company** and a specific **opportunity**.
- **Relations:**
  - Belongs to a **granter_company**.
  - Belongs to a **granter_opportunity**.
  - Has associated **granter_applicationfiles** (files relevant to this application).
---
### **granter_applicationfile**
- Files tied to a specific **application**.
- Usually provide company or project-specific context for that application.
- **Relations:**
  - Belongs to a **granter_application**.
---
### **granter_companyfile**
- Files that contain general company context (used for RAG purposes).
- **Relations:**
  - Belongs to a **granter_company**.
---
### **granter_companymemory**
- Small text snippets stored as vectors for RAG purposes.
- Help provide semantic context when drafting applications.
- **Relations:**
  - Belongs to a **granter_company**.
---
### **granter_opportunity**
- Represents a funding opportunity (grant, tax incentive, investment, or loan).
- **Relations:**
  - Can have multiple **granter_applications** from different companies.
  - Has associated **granter_opportunityfiles**.
  - Has associated **granter_timelines** (opening dates, deadlines, etc.).
  - Has associated **granter_eligibilitycriterias** (eligibility requirements to apply).
---
### **granter_opportunityfile**
- Files linked to a specific **opportunity**.
- Provide contextual information for RAG when drafting or evaluating applications.
- **Relations:**
  - Belongs to a **granter_opportunity**.
---
### **granter_generalopportunityfile**
- Files that are not tied to a single opportunity.
- Provide context across **multiple opportunities**.
---
### **granter_timeline**
- Represents important dates for an **opportunity** (opening, submission deadlines, evaluations, etc.).
- **Relations:**
  - Belongs to a **granter_opportunity**.
---
### **granter_consortium**
- Represents a consortium formed by multiple companies.
- Used to apply to opportunities jointly.
- **Relations:**
  - Can include multiple **granter_consortiumpartners**.
  - Can be linked to **granter_applications** when a consortium applies instead of a single company.
---
### **granter_consortiumpartner**
- Represents a company persona or role within a **consortium** (e.g., lead applicant, research partner, SME partner).
- **Relations:**
  - Belongs to a **granter_consortium**.
  - Each partner is typically a **granter_company**.
---
### **granter_eligibilitycriteria**
- Defines the eligibility criteria for an **opportunity**.
- Examples: financial status, company size, sector, geographic location.
- **Relations:**
  - Belongs to a **granter_opportunity**.
  - Has multiple **granter_matchchecks** for individual companies.
---
### **granter_matchcheck**
- Represents the eligibility result of a single **company** against a single **eligibility criteria**.
- **Relations:**
  - Belongs to a **granter_company**.
  - Belongs to a **granter_eligibilitycriteria**.
  - Is grouped into a **granter_matchgroup**.
---
### **granter_matchgroup**
- The overall eligibility evaluation of a **company** for an **opportunity**.
- Includes all individual **granter_matchchecks** for that company and opportunity.
- **Relations:**
  - Belongs to a **granter_company**.
  - Belongs to a **granter_opportunity**.
  - Aggregates multiple **granter_matchchecks**.
---
## Summary
- **Companies** apply to **opportunities** by creating **applications**.
- **Files and memories** enrich both companies and opportunities with context for AI-driven drafting (RAG).
- **Eligibility criteria** determine whether a company qualifies for an opportunity:
  - Individual checks are stored in **matchchecks**.
  - The grouped decision is stored in a **matchgroup**.
- **Consortiums** allow multiple companies to join forces and apply together.
- **Timelines** define key dates for opportunities.
This schema ensures that Granter can handle complex funding scenarios, provide accurate context for AI agents, and streamline the grant application process
