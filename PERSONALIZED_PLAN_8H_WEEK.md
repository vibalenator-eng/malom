# PERSONALIZED DEVELOPMENT PLAN
## Balazs' Tech Mastery & Product Launch
**Assessment Results Summary:**
- Python & Backend: 4/25 (Some experience)
- Databases & SQL: 2/25 (Very beginner)
- Frontend & UI: 1/25 (Minimal)
- DevOps & Infrastructure: 7/25 (Beginner)
- API & Web Standards: 2/25 (Very beginner)
- Git & Version Control: 3/25 (Very beginner)
- AI & LLM: 2/25 (Very beginner)
- **Project Management: 9/25 (Intermediate - Your Strength!)**

**Overall Score: 30/200 = BEGINNER PATH** ✓

**Key Insight:** You have project management skills to lead this. Technology is learnable. We'll build the app AND your tech skills in parallel.

**Additional Learning Focus:** As the product grows, we'll add real-time communication patterns: MQTT for lightweight event messaging, WebSockets for live updates, and RPC-style request/response flows for commands and control.

---

## PHASE 0: FOUNDATION WEEK (Week 1)
**Goal:** Setup, establish rituals, virtual team roles  
**Time Commitment:** 8 hours (compressed first week)

### 0.1 Development Environment Setup (2.5 hours)

**Task 0.1.1: Install Core Tools** [30 min]
```bash
EXPLICIT CHECKLIST:
☐ Python 3.10+ (https://www.python.org/downloads/)
  └─ Verify: Open PowerShell, type: python --version
  └─ Expected output: Python 3.10.x or 3.11.x

☐ VS Code (https://code.visualstudio.com/)
  └─ Extensions to install (Ctrl+Shift+X in VS Code):
     ☐ Python (Microsoft)
     ☐ Pylance
     ☐ Thunder Client (for API testing)
     ☐ GitLens
     ☐ Docker

☐ Git (https://git-scm.com/)
  └─ Verify: Open PowerShell, type: git --version

☐ Docker Desktop (https://www.docker.com/products/docker-desktop)
  └─ Verify: Open PowerShell, type: docker --version

☐ PostgreSQL (https://www.postgresql.org/download/)
  └─ OR use Docker Compose instead (we'll setup in Phase 1)

TOTAL TIME: 30 minutes
```

**Task 0.1.2: Verify Installation** [15 min]
```bash
# Open PowerShell and run these commands:
python --version           # Should be 3.10+
git --version              # Should be 2.3+
docker --version           # Should be 20.x+

# All should show version numbers. If not, reinstall that tool.
```

**Task 0.1.3: Clone Repository & Setup Workspace** [45 min]
```bash
# PowerShell commands:
cd Desktop  # or your preferred location

git clone https://github.com/vibalenator-eng/malom.git
cd malom

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# You should see (venv) at the start of your PowerShell line

# Install current dependencies
pip install -r requirements.txt

# Verify Flask runs
python app.py
# Should see: "Running on http://127.0.0.1:5000"
# Press Ctrl+C to stop
```

**DEFINITION - Virtual Environment:**
A sandboxed Python installation for your project. Prevents conflicts between projects. Always activate before working.

---

### 0.2 GitHub Setup & Project Management (2.5 hours)

**Task 0.2.1: Create GitHub Project Board** [45 min]

**Step 1: Create project**
1. Go to: https://github.com/vibalenator-eng/malom
2. Click "Projects" tab
3. Click "New project"
4. Name: "Malom Pro - 2026"
5. Template: "Table" (easier for tracking)
6. Click "Create project"

**Step 2: Configure columns**
```
Columns to create (left to right):
┌─────────────┬──────────────┬─────────────┬──────────────┐
│ Backlog     │ Ready        │ In Progress │ Done         │
│ (not ready) │ (scheduled)  │ (working)   │ (completed)  │
└─────────────┴──────────────┴─────────────┴──────────────┘

Add fields:
- Priority: Low / Medium / High
- Estimated Hours: number
- Assigned To: You, Architect, DevOps, PM
```

**Task 0.2.2: Create GitHub Issues for Phase 1** [45 min]

**Issue Template (copy this for each):**
```markdown
# TITLE: [Phase][Component] Brief description

## Description
One clear sentence explaining what needs to be done.

## Acceptance Criteria
- [ ] Specific, testable outcome 1
- [ ] Specific, testable outcome 2
- [ ] Specific, testable outcome 3

## Assigned To
(Architect / DevOps / PM)

## Estimated Hours
(Number)

## Link to Documentation
(URL or file path)
```

**Create these 6 issues:**
1. **[Phase1] Architecture - Database Schema Design**
   - Acceptance: ERD diagram created, SQL scripts written
   - Assigned: Architect
   - Hours: 3

2. **[Phase1] Architecture - API Specification**
   - Acceptance: OpenAPI (Swagger) spec written for all endpoints
   - Assigned: Architect
   - Hours: 4

3. **[Phase1] Backend - Project Structure**
   - Acceptance: Flask project scaffold created with blueprint structure
   - Assigned: DevOps
   - Hours: 2

4. **[Phase1] DevOps - Docker Setup**
   - Acceptance: Dockerfile, docker-compose.yml working locally
   - Assigned: DevOps
   - Hours: 3

5. **[Phase1] Backend - User Model & Database**
   - Acceptance: User table created, SQLAlchemy model works
   - Assigned: Architect
   - Hours: 4

6. **[Phase1] PM - Risk Assessment & Timeline**
   - Acceptance: Risk register created, weekly schedule written
   - Assigned: PM
   - Hours: 2

**Task 0.2.3: Setup GitHub Actions (Basic)** [30 min]

Create file: `.github/workflows/basic-tests.yml`

```yaml
name: Basic Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest tests/ -v
```

**DEFINITION - GitHub Actions:**
Automation that runs when you push code. Tests automatically, reports failures. Saves you from manual testing.

---

### 0.3 Virtual Team Roles Definition (2 hours)

**EXPLICIT DEFINITION OF YOUR VIRTUAL TEAM:**

### **Role 1: Balazs-Architect** (You, wearing design hat)
**Responsibilities:**
- Design system architecture
- Make technology choices
- Review code quality
- Teach concepts when stuck
- Write documentation specs

**When you're this role:**
- Thinking about HOW the system works
- Designing databases, APIs
- Making decisions (tech stack, patterns)
- Writing detailed specs

**Decision Log Template:**
```
DECISION: [Brief title]
CONTEXT: Why we're making this decision
OPTIONS CONSIDERED:
  1. Option A (pros/cons)
  2. Option B (pros/cons)
DECISION: We chose [X] because [reasons]
CONSEQUENCES: What this means for future work
DATE: YYYY-MM-DD
```

---

### **Role 2: Balazs-DevOps** (You, wearing infrastructure hat)
**Responsibilities:**
- Setup development environment
- Build Docker containers
- Setup CI/CD pipelines
- Deploy to hosting
- Troubleshoot environment issues

**When you're this role:**
- Setting up tools
- Running commands in terminal
- Building containers
- Deploying code

**Infrastructure Checklist Template:**
```
ENVIRONMENT: [Local / Staging / Production]
SETUP DATE: YYYY-MM-DD
☐ Dependencies installed
☐ Environment variables set
☐ Database initialized
☐ Can start app without errors
TESTED BY: [Date]
NEXT STEP: [What to do next]
```

---

### **Role 3: Balazs-PM** (You, wearing project management hat)
**Responsibilities:**
- Weekly planning & scheduling
- Track progress in GitHub Projects
- Identify risks & dependencies
- Adjust timeline based on reality
- Coordinate between Architect & DevOps
- Manage your 8h/week budget

**When you're this role:**
- Planning the week
- Updating project board
- Assessing if on track
- Making timeline decisions

**Weekly PM Checklist:**
```
WEEK: [Date range]
HOURS AVAILABLE: 8h

PLANNED TASKS:
☐ Task 1 (est. 2h)
☐ Task 2 (est. 3h)
☐ Task 3 (est. 2.5h)
Total: 7.5h

ACTUAL HOURS USED: [Track as you work]

COMPLETED THIS WEEK:
- [Task 1: Done/Blocked/Partial]
- [Task 2: Done/Blocked/Partial]

BLOCKERS:
- [If anything is stuck, list here]

NEXT WEEK PLAN:
- [What's the priority?]

LEARNING ACQUIRED THIS WEEK:
- [What did you learn?]
```

---

### 0.4 Establish Weekly Ritual (1 hour)

**EVERY FRIDAY (or end of week):**
```
TIME NEEDED: 30 minutes
RITUAL:

Step 1: Review This Week (10 min)
  └─ Open GitHub Projects board
  └─ Count cards in "Done" column
  └─ Write down accomplishments
  └─ Identify blockers
  └─ Update actual hours in checklist

Step 2: Plan Next Week (15 min)
  └─ Look at "Ready" column
  └─ Pick tasks that fit 8 hours
  └─ Drag into "In Progress" (don't pull more than fits!)
  └─ Estimate if realistic
  └─ Adjust if needed

Step 3: Reflect on Learning (5 min)
  └─ What did you learn this week?
  └─ What was confusing?
  └─ What surprised you?
  └─ Write in a learning journal (optional but recommended)

SAVE THIS AS RECURRING CALENDAR EVENT
```

---

## PHASE 1: ARCHITECTURE & FOUNDATION (Weeks 2-3)
**Goal:** Design system properly before coding  
**Time Commitment:** 16 hours (8h/week × 2 weeks)  
**Deliverables:** Database design, API spec, Docker setup

### 1.1 Database Schema Design (Architect Role) [3 hours]

**EXPLICIT PROCESS:**

**Step 1.1.1: Identify Entities [1 hour]**

DEFINITION - Entity: A "thing" in your system (User, Game, Chat Message, etc.)

```
ENTITIES FOR MALOM PRO:

1. USER
   └─ What we need to remember:
      ├─ username (text, unique)
      ├─ email (text, unique)
      ├─ password (hashed text)
      ├─ created_date (date)
      ├─ is_active (yes/no)
      └─ profile_type (player/professional/admin)

2. GAME
   └─ What we need to remember:
      ├─ game_id (unique number)
      ├─ player1_id (which user)
      ├─ player2_id (which user)
      ├─ game_state (JSON - board positions)
      ├─ started_date (date)
      ├─ ended_date (date)
      ├─ winner_id (which user won)
      └─ difficulty_level (1-5)

3. CHAT_MESSAGE
   └─ What we need to remember:
      ├─ message_id (unique)
      ├─ user_id (who wrote it)
      ├─ content (text)
      ├─ created_date (date)
      ├─ is_from_balazs (yes/no)
      └─ conversation_id (which chat thread)

4. PORTFOLIO_ITEM
   └─ What we need to remember:
      ├─ item_id (unique)
      ├─ user_id (whose portfolio)
      ├─ title (text)
      ├─ description (text)
      ├─ url (link)
      ├─ category (project/article/achievement)
      └─ created_date (date)

5. PERSONALITY_TRAIT (for Balazs AI)
   └─ What we need to remember:
      ├─ trait_id (unique)
      ├─ trait_name (text: humor, patience, etc)
      ├─ trait_value (1-5 scale)
      ├─ last_updated (date)
      └─ feedback_score (how well is it working?)
```

**Step 1.1.2: Define Relationships [1 hour]**

DEFINITION - Relationship: How entities connect to each other

```
RELATIONSHIPS (using arrows):

USER ←→ GAME
  └─ One user can have many games
  └─ One game has two users
  └─ SQL: game.player1_id → user.user_id
  └─ SQL: game.player2_id → user.user_id

USER ←→ CHAT_MESSAGE
  └─ One user writes many messages
  └─ One message written by one user
  └─ SQL: chat_message.user_id → user.user_id

USER ←→ PORTFOLIO_ITEM
  └─ One user has many portfolio items
  └─ One item belongs to one user
  └─ SQL: portfolio_item.user_id → user.user_id

USER ←→ PERSONALITY_TRAIT
  └─ One user (Balazs) has many traits
  └─ SQL: personality_trait.user_id → 1 (hardcoded for Balazs)
```

**Step 1.1.3: Create ERD Diagram [1 hour]**

Use Draw.io (https://draw.io) or Excalidraw (https://excalidraw.com)

**Save file as:** `docs/ERD_DATABASE.png`

**Diagram should look like:**
```
┌─────────────────┐         ┌─────────────────┐
│     USER        │         │      GAME       │
├─────────────────┤         ├─────────────────┤
│ user_id (PK)*   │◄────────│ game_id (PK)    │
│ username        │   1:N   │ player1_id (FK) │
│ email           │         │ player2_id (FK) │
│ password_hash   │         │ game_state      │
│ created_date    │         │ winner_id (FK)  │
│ profile_type    │         │ started_date    │
└─────────────────┘         └─────────────────┘
        │
        │ 1:N
        ├──────────────────────┐
        │                      │
        v                      v
┌─────────────────────┐  ┌──────────────────┐
│  CHAT_MESSAGE       │  │ PORTFOLIO_ITEM   │
├─────────────────────┤  ├──────────────────┤
│ message_id (PK)     │  │ item_id (PK)     │
│ user_id (FK)        │  │ user_id (FK)     │
│ content             │  │ title            │
│ created_date        │  │ description      │
│ is_from_balazs      │  │ url              │
│ conversation_id     │  │ category         │
└─────────────────────┘  │ created_date     │
                         └──────────────────┘

Legend:
(PK) = Primary Key (unique identifier)
(FK) = Foreign Key (reference to another table)
1:N = One-to-Many relationship
```

**DELIVERABLE: Save to repo** `docs/DATABASE_DESIGN.md`
```markdown
# Database Design Document

## Overview
Malom Pro uses PostgreSQL with 5 main entities.

## Entity Relationship Diagram
[Include the ERD image]

## Entities

### USER
| Field | Type | Notes |
|-------|------|-------|
| user_id | SERIAL PRIMARY KEY | Auto-increment |
| username | VARCHAR(50) UNIQUE | Required |
| email | VARCHAR(100) UNIQUE | Required |
| password_hash | VARCHAR(255) | Bcrypt hashed |
| created_date | TIMESTAMP | DEFAULT NOW() |
| is_active | BOOLEAN | DEFAULT true |
| profile_type | VARCHAR(20) | player/professional/admin |

[Continue for other entities...]

## Relationships
- User 1:N Game (user can play many games)
- User 1:N ChatMessage (user can send many messages)
- User 1:N PortfolioItem (user can have many items)

## Notes
- All datetimes are UTC
- All IDs are auto-incrementing integers
- Foreign keys have ON DELETE CASCADE for cleanup
```

---

### 1.2 REST API Specification (Architect Role) [4 hours]

DEFINITION - REST API: Web interface for programs to talk to each other using HTTP requests

**Step 1.2.1: List All Endpoints [2 hours]**

Use this template for EVERY endpoint:

```
ENDPOINT: [HTTP METHOD] /api/[resource]/[action]
├─ Purpose: [One sentence]
├─ Authentication: Required / Optional / None
├─ Input Parameters:
│  └─ name: type, required/optional, description
├─ Success Response (200):
│  └─ {
│      "status": "success",
│      "data": { ... }
│    }
├─ Error Response (400/401/500):
│  └─ {
│      "status": "error",
│      "message": "Human-readable error"
│    }
└─ Example:
   Request: curl -X GET http://localhost:5000/api/users/me
   Response: { "status": "success", "data": { "username": "balazs" } }
```

**COMPLETE API ENDPOINT LIST:**

**AUTHENTICATION**
```
1. POST /api/auth/register
   Purpose: Create new user account
   Input: username, email, password
   Output: user_id, token

2. POST /api/auth/login
   Purpose: Login user
   Input: username, password
   Output: token, user

3. POST /api/auth/logout
   Purpose: Logout (clear token)
   Input: token
   Output: { status: "success" }

4. GET /api/auth/me
   Purpose: Get current logged-in user
   Input: token (in header)
   Output: user object
```

**GAMES**
```
5. GET /api/games
   Purpose: List all games user played
   Input: token
   Output: [games array]

6. POST /api/games
   Purpose: Start new game
   Input: token, difficulty (1-5)
   Output: game_id

7. GET /api/games/{game_id}
   Purpose: Get current game state
   Input: game_id
   Output: board state, whose turn, legal moves

8. POST /api/games/{game_id}/move
   Purpose: Play a move
   Input: token, game_id, source, destination
   Output: new game state

9. GET /api/games/{game_id}/moves
   Purpose: Get legal moves
   Input: game_id
   Output: [moves array]
```

**CHAT (Balazs)**
```
10. GET /api/chat/messages
    Purpose: Get conversation history
    Input: token, limit (optional)
    Output: [messages array]

11. POST /api/chat/message
    Purpose: Send message to Balazs
    Input: token, message_text
    Output: { user_message, balazs_response }

12. DELETE /api/chat/clear
    Purpose: Clear conversation history
    Input: token
    Output: { status: "success" }
```

**PORTFOLIO**
```
13. GET /api/portfolio
    Purpose: List portfolio items (your own or public)
    Input: user_id (optional)
    Output: [items array]

14. POST /api/portfolio
    Purpose: Create portfolio item
    Input: token, title, description, url, category
    Output: item_id

15. PUT /api/portfolio/{item_id}
    Purpose: Update portfolio item
    Input: token, item_id, updated fields
    Output: updated item

16. DELETE /api/portfolio/{item_id}
    Purpose: Delete portfolio item
    Input: token, item_id
    Output: { status: "success" }
```

**USER**
```
17. GET /api/users/{user_id}
    Purpose: Get user profile
    Input: user_id
    Output: username, profile_type, portfolio count

18. PUT /api/users/me
    Purpose: Update own profile
    Input: token, updated fields
    Output: updated user
```

**Step 1.2.2: Write OpenAPI Specification [2 hours]**

Create file: `docs/openapi.yaml`

```yaml
openapi: 3.0.0
info:
  title: Malom Pro API
  version: 1.0.0
  description: REST API for Malom game, portfolio, and Balazs chat

servers:
  - url: http://localhost:5000/api
    description: Local development
  - url: https://malom-pro.app/api
    description: Production

paths:
  /auth/login:
    post:
      summary: User login
      tags: [Authentication]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
              required: [username, password]
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: success
                  data:
                    type: object
                    properties:
                      token:
                        type: string
                      user_id:
                        type: integer

  /games:
    get:
      summary: List user's games
      tags: [Games]
      security:
        - BearerAuth: []
      responses:
        '200':
          description: List of games
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                  data:
                    type: array
                    items:
                      type: object
    post:
      summary: Start new game
      tags: [Games]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                difficulty:
                  type: integer
                  minimum: 1
                  maximum: 5
      responses:
        '201':
          description: Game created

# Continue for all endpoints...

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        user_id:
          type: integer
        username:
          type: string
        email:
          type: string
        profile_type:
          type: string
          enum: [player, professional, admin]
        created_date:
          type: string
          format: date-time

    Game:
      type: object
      properties:
        game_id:
          type: integer
        player1_id:
          type: integer
        player2_id:
          type: integer
        game_state:
          type: object
        status:
          type: string
          enum: [active, finished]
```

**DELIVERABLE:** Save to repo as `docs/openapi.yaml`

---

### 1.3 DevOps: Docker & Docker Compose (DevOps Role) [3 hours]

DEFINITION - Docker: Package entire app into portable containers. Same everywhere.

**Step 1.3.1: Understand Docker Concepts [30 min] (Reading)**

CONCEPTS:
```
IMAGE: Blueprint (like a recipe)
  └─ Contains: OS, Python, dependencies, code
  └─ Immutable (doesn't change once built)
  └─ Can create many containers from one image

CONTAINER: Running instance (like a cake from a recipe)
  └─ Temporary (deleted when stopped)
  └─ Independent (can't affect other containers)
  └─ Has its own filesystem, processes, network

DOCKERFILE: Text file describing how to build an image
  └─ Step-by-step instructions
  └─ "Start with Ubuntu, install Python, copy code, run server"

DOCKER COMPOSE: Run multiple containers together
  └─ Database container
  └─ Web app container
  └─ Redis cache container
  └─ All configured in one file
```

**Read:** https://docs.docker.com/get-started/ (30 min)

**Step 1.3.2: Create Dockerfile [1 hour]**

File: `Dockerfile` (in project root)

```dockerfile
# Start from official Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app code
COPY . .

# Expose port (document, doesn't actually expose)
EXPOSE 5000

# Command to run when container starts
CMD ["python", "app.py"]
```

**Explanation line-by-line:**
```
FROM python:3.10-slim
  └─ Use official Python 3.10 image (slim = smaller size)

WORKDIR /app
  └─ Inside container, create /app folder and use it

COPY requirements.txt .
  └─ Copy requirements.txt from YOUR computer to container's /app

RUN pip install --no-cache-dir -r requirements.txt
  └─ Inside container, install all Python packages
  └─ --no-cache-dir = save space

COPY . .
  └─ Copy all files from YOUR computer to container's /app

EXPOSE 5000
  └─ Document that app listens on port 5000
  └─ Doesn't actually expose (that's docker-compose's job)

CMD ["python", "app.py"]
  └─ When container starts, run: python app.py
```

**Step 1.3.3: Create docker-compose.yml [1 hour]**

File: `docker-compose.yml` (in project root)

```yaml
# Docker Compose: Run multiple services together
version: '3.8'

services:
  # Web application service
  web:
    build: .  # Build from Dockerfile in current directory
    ports:
      - "5000:5000"  # Map port 5000 on YOUR computer to 5000 in container
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://malom:password@db:5432/malom_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - .:/app  # Sync local files to container (changes reflected live)
    command: python app.py

  # PostgreSQL database service
  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_USER=malom
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=malom_db
    ports:
      - "5432:5432"  # Only for local debugging
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Persist data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U malom"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis cache service (for sessions, caching)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"  # Only for local debugging
    volumes:
      - redis_data:/data

# Persistent volumes (data survives container restarts)
volumes:
  postgres_data:
  redis_data:
```

**Explanation:**
```
services:
  └─ List of containers to run

web:
  └─ Our Flask app container
  └─ build: . means use Dockerfile in this directory
  └─ ports: 5000:5000 means "from my computer's 5000, go to container's 5000"
  └─ depends_on: Start db and redis BEFORE starting web
  └─ volumes: - .:/app means "sync my current folder to container's /app"

db:
  └─ PostgreSQL database container
  └─ Uses pre-built postgres:14-alpine image (don't need Dockerfile)
  └─ POSTGRES_USER/PASSWORD/DB: Initial setup
  └─ volumes: postgres_data:/var/lib/postgresql/data saves DB even if container deleted

redis:
  └─ Redis cache (fast key-value store)
  └─ Used for sessions, temporary data

volumes:
  └─ postgres_data and redis_data are persistent
  └─ Survive if containers stop/restart
```

**Step 1.3.4: Test Docker Setup [30 min]**

**In PowerShell:**
```bash
# Navigate to project folder
cd path/to/malom

# Build and start all services
docker-compose up

# You should see logs like:
# web_1   | Running on http://0.0.0.0:5000
# db_1    | database system is ready to accept connections

# Leave it running for now (Ctrl+C to stop)

# In another PowerShell window:
docker-compose ps  # Should see web, db, redis all "Up"

# Stop everything gracefully
docker-compose down
```

**DELIVERABLE:** Both files committed to repo
```
☐ Dockerfile created
☐ docker-compose.yml created
☐ Tested locally: docker-compose up works
☐ Verified: services start without errors
```

---

### 1.4 Real-Time Communication & Event-Driven Patterns (Architect Role) [3 hours]

DEFINITION - REAL-TIME COMMUNICATION: Patterns for live, low-latency interaction between app services, browser clients, and devices.

**Step 1.4.1: Learn the Core Concepts [1 hour]**

**Concepts to understand:**
- MQTT: Publish/subscribe messaging for lightweight telemetry, device events, and simple event fan-out
- WebSockets: Full-duplex, real-time communication for live game updates, chat, and status streams
- RPC (Remote Procedure Call): Request/response pattern for commands like "start game", "move piece", or "send chat"

**Suggested learning order:**
1. Understand topics and when each pattern is appropriate
2. Compare MQTT vs WebSockets vs RPC for Malom use cases
3. Choose one simple proof-of-concept for the MVP

**Step 1.4.2: Map the Patterns to Malom Pro [1 hour]**

**Recommended use cases for this project:**
- MQTT: send lightweight events like "game started", "player joined", or "system alert"
- WebSockets: live game board updates, Balazs chat streaming, and real-time UI sync
- RPC: trigger server actions such as "create game", "make move", or "clear conversation"

**Decision template:**
```
DECISION: Real-time pattern choice
CONTEXT: We need live interaction without overcomplicating the MVP
OPTIONS CONSIDERED:
  1. Pure REST only
  2. REST + WebSockets
  3. MQTT + WebSockets + RPC
DECISION: We will use WebSockets for live UI updates and RPC-style commands, and keep MQTT as an optional later step for lightweight event messaging.
CONSEQUENCES: The MVP stays simpler, while the architecture remains extensible.
```

**Step 1.4.3: Build a Small Proof of Concept [1 hour]**

**Goal:** Prove the concept locally before adding it to the app.

**Minimal POC ideas:**
- WebSocket echo server: client sends message, server returns it instantly
- RPC-style endpoint: POST /api/game/action and receive a structured response
- MQTT topic test: publish and subscribe to a test topic locally

**Deliverables:**
- Save to repo: `docs/REALTIME_ARCHITECTURE.md`
- Create a simple local proof-of-concept script or endpoint
- Write 3 bullets explaining when to use MQTT, WebSockets, and RPC

---

### 1.5 Project Management: Risk Assessment (PM Role) [2 hours]

**Step 1.4.1: Identify Risks [1 hour]**

DEFINITION - Risk: Something that MIGHT go wrong

**Risk Register Template:**
```
RISK ID | DESCRIPTION | PROBABILITY | IMPACT | MITIGATION
--------|-------------|-------------|--------|------------
R1      | [description] | 1-5 | 1-5 | [action]
        | Score = P × I | (1=low) | (1=low) |
```

**Common Risks for THIS Project:**

| ID | Risk | Prob | Impact | Mitigation |
|----|------|------|--------|-----------|
| R1 | Only 8h/week - not enough time | 4 | 3 | Scope to MVP only, prioritize ruthlessly |
| R2 | Database schema wrong - need redesign | 3 | 4 | Get design right now (Phase 1), use ERD |
| R3 | LM Studio too complex (Balazs AI) | 4 | 3 | Start simple, use curl before Python |
| R4 | Learning overwhelm (too many techs) | 4 | 4 | Learn by doing, one thing at a time |
| R5 | Deployment to hosting fails | 2 | 3 | Test Docker locally first, use free tiers |
| R6 | GitHub Actions pipeline breaks | 2 | 2 | Use pre-built actions, test locally |
| R7 | PostgreSQL data lost | 1 | 5 | Use docker volumes, backup regularly |

**Create file:** `docs/RISK_REGISTER.md`

```markdown
# Risk Register - Malom Pro

## Overview
Living document updated weekly. Identifies, assesses, mitigates risks.

## Risk Matrix
| ID | Risk | Probability | Impact | Score | Status | Mitigation |
|----|------|-------------|--------|-------|--------|-----------|
| R1 | Time constraint (8h/week only) | 4/5 | 3/5 | 12 | Active | MVP scope, prioritize ruthlessly |
| R2 | Database redesign needed mid-project | 3/5 | 4/5 | 12 | Active | Finalize schema now, document decisions |
| R3 | LLM (Balazs) implementation too complex | 4/5 | 3/5 | 12 | Active | Start with simple prompts, iterate |
| R4 | Learning overwhelm (many new techs) | 4/5 | 4/5 | 16 | CRITICAL | Learn by doing, one tech per phase |
| R5 | Frontend (React) slow to develop | 4/5 | 2/5 | 8 | Active | Use templates, component library |
| R6 | Deployment/hosting issues | 2/5 | 3/5 | 6 | Managed | Test locally in Docker first |
| R7 | Data loss (database) | 1/5 | 5/5 | 5 | Managed | Use persistent volumes, backups |

## Mitigation Details

### R4: Learning Overwhelm (CRITICAL)
**Actions:**
- [ ] Learn one tech deeply per phase (not all at once)
- [ ] Use structured learning path (this document)
- [ ] When stuck > 30 min: ask for help, don't continue stuck
- [ ] Review learning acquired weekly
- [ ] Take breaks (prevent burnout)

### R3: LLM Complexity
**Actions:**
- [ ] Start with curl/Thunder Client to test LM Studio
- [ ] Simple prompt first: "Hello" → get response
- [ ] Don't build Balazs personality until basics work
- [ ] Phase 4 dedicated to this (not now)

### R1: Time Constraint
**Actions:**
- [ ] Define MVP (absolute minimum)
- [ ] Use GitHub Projects to track 8h/week
- [ ] If drifting, cut features (not quality)
- [ ] Weekly review with PM role

## Updates
- Week 1 (July 18): Initial register created
- [Add updates as you go]
```

**Step 1.4.2: Create 8-Week Timeline [1 hour]**

**File:** `docs/TIMELINE.md`

```markdown
# Development Timeline - Malom Pro
## 8 Hours/Week × 14 Weeks = 112 Total Hours

### PHASE 1: FOUNDATION (Weeks 1-2, 16h)
**Goal:** Design & setup complete

**Week 1 (July 18-24):** Setup
- [ ] Dev environment (Python, Docker, Git)
- [ ] GitHub project board
- [ ] Virtual team roles defined
- Est: 8 hours

**Week 2 (July 25-31):** Architecture
- [ ] Database design finalized
- [ ] API specification written
- [ ] Docker setup working
- [ ] Risk register created
- Est: 8 hours

### PHASE 2: MVP BACKEND (Weeks 3-4, 16h)
**Goal:** API working, database functional

**Week 3 (Aug 1-7):**
- [ ] Flask project scaffolding
- [ ] User authentication (register/login)
- [ ] PostgreSQL connection working
- [ ] First API endpoints
- Est: 8 hours

**Week 4 (Aug 8-14):**
- [ ] Game API endpoints
- [ ] Real-time transport prototype (WebSocket echo or RPC-style command flow)
- [ ] Unit tests (80%+ coverage)
- [ ] Documentation generated
- Est: 8 hours

### PHASE 3: MVP FRONTEND (Weeks 5-6, 16h)
**Goal:** Web UI working with backend

**Week 5 (Aug 15-21):**
- [ ] React project setup
- [ ] Landing page component
- [ ] Login/register UI
- Est: 8 hours

**Week 6 (Aug 22-28):**
- [ ] Game board UI
- [ ] Connect to backend API
- [ ] Basic styling
- Est: 8 hours

### PHASE 4: AI CHAT (Weeks 7-8, 16h)
**Goal:** Balazs chatbot working

**Week 7 (Aug 29-Sep 4):**
- [ ] LM Studio setup locally
- [ ] Chat API endpoints
- [ ] Simple personality prompts
- Est: 8 hours

**Week 8 (Sep 5-11):**
- [ ] Chat UI component
- [ ] Conversation history
- [ ] Lightweight MQTT/WebSocket event test for live updates
- [ ] Personality evaluation framework
- Est: 8 hours

### PHASE 5: PORTFOLIO (Weeks 9-10, 16h)
**Goal:** Portfolio pages working

**Week 9 (Sep 12-18):**
- [ ] Portfolio API
- [ ] Portfolio UI pages
- [ ] Admin CMS basics
- Est: 8 hours

**Week 10 (Sep 19-25):**
- [ ] Markdown support for content
- [ ] SEO basics
- [ ] Portfolio content created
- Est: 8 hours

### PHASE 6: DEPLOYMENT (Weeks 11-12, 16h)
**Goal:** Live on web + desktop

**Week 11 (Sep 26-Oct 2):**
- [ ] GitHub Actions CI/CD pipeline
- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Vercel
- Est: 8 hours

**Week 12 (Oct 3-9):**
- [ ] PyQt desktop app skeleton
- [ ] Desktop/web sync
- [ ] Raspberry Pi Docker setup
- Est: 8 hours

### PHASE 7: POLISH (Weeks 13-14, 16h)
**Goal:** Production-ready

**Week 13 (Oct 10-16):**
- [ ] Documentation complete
- [ ] Code quality review
- [ ] Performance optimization
- Est: 8 hours

**Week 14 (Oct 17-23):**
- [ ] Launch & announcement
- [ ] User testing
- [ ] Bug fixes
- [ ] Retrospective
- Est: 8 hours

## CRITICAL PATH
```
Setup → Architecture → Backend → Frontend → Chat → Deploy → Polish
(1w)      (1w)          (2w)      (2w)      (2w)   (2w)    (2w)
```

If ANY of these phases slip, rest of timeline affects.

## CONTINGENCY
- If Phase 3 (Frontend) takes extra week: Reduce portfolio features
- If Phase 4 (Chat) takes extra week: Use simpler personality, iterate later
- Buffer: Last 2 weeks are safety net

## METRICS
Track weekly:
- [ ] Actual hours used vs estimated
- [ ] Tasks completed vs planned
- [ ] Blockers encountered
- [ ] Learning acquired
```

---

### 1.6 Summary: Week 1 Deliverables (Completion Check)

**MUST BE DONE BY END OF WEEK 1:**

```
DEVELOPMENT ENVIRONMENT:
☐ Python 3.10+ installed & verified
☐ VS Code installed with Python extension
☐ Git installed & verified
☐ Docker Desktop installed & verified
☐ Malom repo cloned locally
☐ Virtual environment created & working
☐ Flask app runs locally without errors

GITHUB SETUP:
☐ GitHub Projects board created
☐ 6 Phase 1 issues created
☐ Basic GitHub Actions workflow created
☐ Branching strategy documented

VIRTUAL TEAM:
☐ Balazs-Architect role defined
☐ Balazs-DevOps role defined
☐ Balazs-PM role defined
☐ Weekly ritual scheduled

DOCUMENTATION:
☐ This plan saved locally
☐ Risk register started
☐ Timeline created
☐ Friday review checklist ready

CONFIDENCE CHECK:
☐ Understand Docker concepts
☐ Know what API spec is
☐ Know what database schema is
☐ Ready to start Week 2
```

---

## PHASE 1: DETAILED WEEK 2 (Weeks 2-3 of Project = Aug 1-14)

### OBJECTIVE
Complete all architecture & design before writing main code.

### WEEK 2 TASKS (ARCHITECT ROLE)

**DAYS 1-2: Database Schema (Refined)**

**Task 1: Create ERD in Draw.io [2 hours]**
1. Go to https://draw.io
2. Create new diagram
3. Create boxes for each entity (USER, GAME, CHAT_MESSAGE, etc.)
4. Add fields in each box
5. Draw relationships between boxes
6. Save as PNG
7. Commit to repo: `docs/erd.png`

**Task 2: Write SQL Create Statements [2 hours]**

File: `backend/sql/001_create_tables.sql`

```sql
-- ============================================
-- MALOM PRO DATABASE SCHEMA
-- ============================================

-- User Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    profile_type VARCHAR(20) DEFAULT 'player', -- player, professional, admin
    bio TEXT,
    avatar_url VARCHAR(255)
);

-- Game Table
CREATE TABLE games (
    game_id SERIAL PRIMARY KEY,
    player1_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    player2_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    game_state JSONB NOT NULL, -- Stores board state as JSON
    difficulty_level INTEGER DEFAULT 3,
    status VARCHAR(20) DEFAULT 'active', -- active, finished, abandoned
    started_date TIMESTAMP DEFAULT NOW(),
    ended_date TIMESTAMP,
    winner_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    moves_count INTEGER DEFAULT 0
);

-- Chat Message Table
CREATE TABLE chat_messages (
    message_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT NOW(),
    is_from_balazs BOOLEAN DEFAULT FALSE,
    conversation_id VARCHAR(100) DEFAULT 'default' -- Group conversations
);

-- Portfolio Item Table
CREATE TABLE portfolio_items (
    item_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50), -- project, article, achievement
    url VARCHAR(255),
    image_url VARCHAR(255),
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW(),
    is_public BOOLEAN DEFAULT TRUE
);

-- Personality Traits Table (for Balazs AI)
CREATE TABLE personality_traits (
    trait_id SERIAL PRIMARY KEY,
    trait_name VARCHAR(100) NOT NULL, -- humor, patience, technical_depth
    trait_value DECIMAL(3,2), -- 1.0 to 5.0 scale
    description TEXT,
    last_updated TIMESTAMP DEFAULT NOW(),
    feedback_score DECIMAL(3,2), -- How well is this trait working? 1-5
    notes TEXT
);

-- Indexes for performance
CREATE INDEX idx_games_player1 ON games(player1_id);
CREATE INDEX idx_games_player2 ON games(player2_id);
CREATE INDEX idx_games_status ON games(status);
CREATE INDEX idx_chat_user ON chat_messages(user_id);
CREATE INDEX idx_chat_date ON chat_messages(created_date);
CREATE INDEX idx_portfolio_user ON portfolio_items(user_id);
```

**Explanation:**
```
SERIAL: Auto-increment integer (1, 2, 3...)
PRIMARY KEY: Unique identifier for this table's rows
REFERENCES: Link to another table (foreign key)
ON DELETE CASCADE: If user deleted, delete all their games too
JSONB: JSON stored as binary (searchable, indexable)
VARCHAR(n): Text field with max n characters
TEXT: Unlimited text
TIMESTAMP: Date and time
BOOLEAN: True/False
Indexes: Speed up searches on frequently-queried fields
```

**DAYS 3-4: API Specification (Refined)**

**Task 3: Write Complete OpenAPI Spec [2 hours]**

File: `docs/openapi.yaml` (create full spec)

Use template from earlier in this document. Save to repo.

**Task 4: Create API Documentation Page [1 hour]**

File: `docs/API_DOCUMENTATION.md`

```markdown
# Malom Pro API Documentation

## Quick Start

### Base URL
- Local: `http://localhost:5000/api`
- Production: `https://malom-pro.app/api`

### Authentication
All endpoints except `/auth/login` and `/auth/register` require:
```
Header: Authorization: Bearer {jwt_token}
```

## Authentication Endpoints

### POST /auth/register
Create new account

**Request:**
```json
{
  "username": "balazs",
  "email": "balazs@example.com",
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "status": "success",
  "data": {
    "user_id": 1,
    "username": "balazs",
    "token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

### POST /auth/login
Login to existing account

**Request:**
```json
{
  "username": "balazs",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "status": "success",
  "data": {
    "user_id": 1,
    "token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

[Continue for all 18 endpoints...]

## Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Request worked |
| 201 | Created | Resource created |
| 400 | Bad Request | Missing field, invalid data |
| 401 | Unauthorized | Token missing/invalid |
| 403 | Forbidden | User doesn't have permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Something broke on server |

## Rate Limiting
- Public endpoints: 100 requests/hour
- Authenticated endpoints: 1000 requests/hour
- Chat endpoint: 50 requests/hour (to avoid LLM spam)

## Versioning
- Current version: v1
- Future: v2 coming in Q4 2026
- All endpoints prefixed with `/api/v1/`
```

### WEEK 2 TASKS (DEVOPS ROLE)

**DAYS 1-3: Docker Finalization**

**Task 5: Build Docker Image** [1 hour]

```bash
# Navigate to project root
cd path/to/malom

# Build image
docker build -t malom:latest .

# Verify image built
docker images  # Should see malom:latest listed

# Run container from image
docker run -p 5000:5000 malom:latest

# Should see Flask starting
# Ctrl+C to stop
```

**Task 6: Test docker-compose** [1 hour]

```bash
# Start all services
docker-compose up

# Verify in another terminal
docker-compose ps  # Should show web, db, redis all Up

# Test database connectivity
docker-compose exec db psql -U malom -d malom_db -c "SELECT 1"
# Should return: 1 (success)

# Stop everything
docker-compose down

# Verify volumes persist
docker-compose up  # DB data should still be there
```

**DAYS 4-5: Documentation**

**Task 7: Create Setup Guide** [1.5 hours]

File: `docs/SETUP.md`

```markdown
# Development Environment Setup

## Prerequisites
- Windows/Mac/Linux
- Git
- Docker Desktop
- 20GB free disk space

## Step 1: Clone Repository
```bash
git clone https://github.com/vibalenator-eng/malom.git
cd malom
```

## Step 2: Configure Environment
Create `.env` file in project root:
```
FLASK_ENV=development
DATABASE_URL=postgresql://malom:password@db:5432/malom_db
REDIS_URL=redis://redis:6379
SECRET_KEY=your-secret-key-here-change-in-production
```

## Step 3: Start Services
```bash
docker-compose up
```

This starts:
- Flask backend on http://localhost:5000
- PostgreSQL on localhost:5432
- Redis on localhost:6379

## Step 4: Initialize Database
```bash
# In another terminal:
docker-compose exec web python -c "from app import create_app; app = create_app(); app.db.create_all()"
```

## Step 5: Test Backend
```bash
curl http://localhost:5000/api/health
```

Should return:
```json
{"status": "ok", "timestamp": "2026-07-18T12:00:00"}
```

## Troubleshooting

### Docker won't start
- Check Docker Desktop is running
- Check no other app is using port 5000, 5432, 6379
- Run: `docker-compose up --build` to rebuild

### Database errors
- Run: `docker-compose down -v` to delete database
- Run: `docker-compose up` to recreate fresh

### Python import errors
- Make sure you're running inside container or virtual environment
- Run: `pip install -r requirements.txt` if outside container
```

### WEEK 2 TASKS (PM ROLE)

**DAYS 1-3: Weekly Planning**

**Task 8: Update Risk Register** [30 min]

Review risks from earlier, update:
- Any new risks identified?
- Any risks resolved?
- Any probabilities changed?

**Task 9: Create Week 3 Plan** [1 hour]

File: `docs/WEEK3_PLAN.md`

```markdown
# Week 3 Plan (Aug 1-7)
## Phase 2 Start: MVP Backend

### Available Time Budget
8 hours this week

### Tasks Planned
1. Flask project scaffolding (2h)
2. User authentication (3h)
3. PostgreSQL connection (1.5h)
4. First API endpoints (1.5h)

Total: 8h

### Success Criteria
- [ ] Flask project structure created
- [ ] User can register via API
- [ ] User can login via API
- [ ] JWT token works
- [ ] Database connection verified
- [ ] No errors in console

### Known Blockers
- Need to understand Flask blueprints
- Need to understand JWT tokens

### Learning Resources
- https://flask.palletsprojects.com/ (Flask docs)
- https://tools.ietf.org/html/rfc7519 (JWT standard)
- Example code: [Will provide]

### Contingency
If JWT takes too long:
- Simplify authentication first
- Use session cookies instead
- Upgrade to JWT in Phase 3
```

**DAYS 4-5: Executive Summary**

**Task 10: Create Project Status Report** [1 hour]

File: `docs/PHASE1_COMPLETION_REPORT.md`

```markdown
# Phase 1 Completion Report
## Foundation & Architecture Complete

**Status:** ✅ COMPLETE
**Duration:** 2 weeks
**Hours Used:** 16h out of 16h planned
**On Schedule:** YES

### Deliverables Completed
- [x] Database schema designed & documented
- [x] ERD diagram created
- [x] SQL create statements written
- [x] REST API specification (OpenAPI)
- [x] Docker setup (Dockerfile + docker-compose.yml)
- [x] GitHub project board configured
- [x] GitHub Actions workflow started
- [x] Risk register established
- [x] Timeline created
- [x] Development environment documented

### Key Decisions Made
1. **Database:** PostgreSQL (scalable, free, reliable)
2. **API:** REST with JWT authentication
3. **Containers:** Docker for local dev + production
4. **Timeline:** 14 weeks, 8h/week

### Risks Managed
- R4 (Learning Overwhelm): Mitigated by structured learning path
- R1 (Time Constraint): Mitigated by ruthless MVP scope

### Lessons Learned
1. Architecture planning saves time later
2. Docker setup now prevents deployment surprises
3. API spec ensures frontend/backend alignment

### Phase 2 Readiness
- [x] Backend team ready to code
- [x] Frontend team ready for API contracts
- [x] DevOps ready for CI/CD
- [ ] Learn requirements clear for all

### Next Steps
1. Start Phase 2: Backend coding
2. Maintain weekly Friday reviews
3. Track actual hours vs estimated
```

---

## SUMMARY: 14-WEEK REALISTIC PATH

### LEARNING PROGRESSION BY PHASE

```
PHASE 1 (Weeks 1-2): PLANNING
└─ Skills: Architecture thinking, Docker basics, API design
└─ You learn: How to plan like an engineer
└─ Output: Complete design before coding

PHASE 2 (Weeks 3-4): PYTHON + BACKEND
└─ Skills: Flask, SQLAlchemy, REST APIs, testing
└─ You learn: Backend development, database
└─ Output: Working API with authentication

PHASE 3 (Weeks 5-6): FRONTEND
└─ Skills: React, JavaScript, CSS
└─ You learn: Frontend development, API consumption
└─ Output: Beautiful web UI connected to backend

PHASE 4 (Weeks 7-8): AI & CHAT
└─ Skills: LLM APIs, prompt engineering, personality design
└─ You learn: How to integrate AI
└─ Output: Balazs chatbot with personality

PHASE 5 (Weeks 9-10): PORTFOLIO
└─ Skills: Content management, SEO, admin panels
└─ You learn: Web application breadth
└─ Output: Professional portfolio section

PHASE 6 (Weeks 11-12): DEVOPS & DEPLOYMENT
└─ Skills: GitHub Actions, Docker deployment, Linux
└─ You learn: Production infrastructure
└─ Output: App running on web, desktop, Raspberry Pi

PHASE 7 (Weeks 13-14): POLISH
└─ Skills: Code quality, documentation, optimization
└─ You learn: Professional practices
└─ Output: Launch-ready product
```

---

## LEARNING STYLE: YOUR PREFERENCES

**You prefer:**
✅ **Explicit, sequential steps** (no assumptions)
✅ **Visual diagrams & flowcharts**
✅ **Clear definitions before examples**
✅ **Detailed specs/documentation**
✅ **Checkboxes & measurable milestones**

**How I'll provide everything:**
1. **Every task has a checklist** - You know when done
2. **Every concept has a definition** - DEFINITION: [term] explains it
3. **Every step is numbered 1, 2, 3...** - No ambiguity
4. **Every diagram is ASCII + description** - Visual + explicit
5. **Every decision is documented** - Why we chose this, not that

---

## NEXT IMMEDIATE ACTIONS

### THIS WEEK (Before You Code):
1. **[ ]** Print or save this document locally
2. **[ ]** Complete all Phase 0 & Week 2 tasks (16 hours)
3. **[ ]** Test everything works locally
4. **[ ]** Schedule Friday review ritual
5. **[ ]** Tell me what questions you have

### QUESTIONS TO CLARIFY:
1. Do you want daily standups or weekly check-ins?
2. Prefer phone/async feedback?
3. Any tech you want to deep-dive FIRST before we start coding?
4. Want me to prepare Week 3 code starter files now?

---

## RESOURCES PROVIDED

**In your repo folder:**
- ✅ PROJECT_PLAN.md (general overview)
- ✅ KNOWLEDGE_ASSESSMENT.md (your score & assessment)
- ✅ THIS DOCUMENT (personalized 14-week plan)

**You create during Phase 0-1:**
- [ ] docs/erd.png (database diagram)
- [ ] docs/DATABASE_DESIGN.md
- [ ] docs/openapi.yaml (API spec)
- [ ] docs/SETUP.md (environment setup)
- [ ] docs/RISK_REGISTER.md
- [ ] docs/TIMELINE.md
- [ ] Dockerfile
- [ ] docker-compose.yml

---

## CONFIDENCE CHECKPOINT

**Before Week 1 ends, you should feel:**
- ✅ Clear on what we're building
- ✅ Confident about the 8h/week pace
- ✅ Understand the 3 virtual team roles
- ✅ Know how to use GitHub Projects
- ✅ Docker running locally without errors
- ✅ Excited to start coding in Week 3

**If you DON'T feel this way: TELL ME.** We adjust.

---

## YOU ARE READY.

This plan is:
- ✅ Realistic (8h/week real, not fantasy)
- ✅ Structured (explicit steps, no assumptions)
- ✅ Achievable (beginner can do this)
- ✅ Measurable (checkboxes, milestones)
- ✅ Professional (enterprise-grade approach)
- ✅ Learning-focused (you grow, product grows)

**Start Phase 0 this week. See you in a week with your progress.**

Good luck! 🚀
