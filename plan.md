# Sprint Plan: Enrollment Helpdesk Assistant

## User Stories

### 1. Incoming Freshman
* **As an** incoming freshman,
* **I want to** quickly check the enrollment requirements and deadlines,
* **So that** I don't miss my slot or submit incomplete documents.
* **Acceptance Criteria:**
  1. Assistant returns a clear list of required documents (e.g., Form 138, Birth Certificate).
  2. Assistant explicitly states the registration deadline date when asked.

### 2. Parent
* **As a** parent of an applicant,
* **I want to** know if tuition can be paid in installments and what scholarships are available,
* **So that** I can plan our family budget for the upcoming semester.
* **Acceptance Criteria:**
  1. Assistant breaks down the installment payment schedule across school terms.
  2. Assistant lists the academic and financial aid scholarships available with basic eligibility.

### 3. Registrar Staff
* **As a** registrar staff member,
* **I want** repetitive informational questions filtered and handled automatically by a chat bot,
* **So that** my team can focus on processing actual documents and manual evaluations.
* **Acceptance Criteria:**
  1. Assistant logs the predicted intent category of every user question into a database/log.
  2. Assistant displays an admin metrics panel showing total questions per category and satisfaction rates.

## Task Backlog
- [x] Task 1: Create PLAN.md with user stories and acceptance criteria (Done)
- [x] Task 2: Write faq.json with 15 entries across 5 categories (Done)
- [x] Task 3: Collect 50 labeled intent data rows in intents.csv (Done)
- [x] Task 4: Develop intent classification model in train.py (Done)
- [x] Task 5: Implement Flask application backend and RAG keyword matching (Done)
- [x] Task 6: Design mobile-responsive UI with chat bubbles and admin dashboard (Done)
- [x] Task 7: Conduct safety guardrail evaluations and record in EVAL.md (Done)
- [x] Task 8: Document project architecture and instructions in README.md (Done)
