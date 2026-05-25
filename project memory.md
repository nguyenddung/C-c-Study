# 🐸 CócStudy — PROJECT MEMORY SNAPSHOT
> **Reconstructed:** 2026-05-25 | **Version:** 0.2.0 | **Status:** Backend ~85% done · Frontend TS layer 0% · Infra 0%

---

## 1. PROJECT OVERVIEW

| Field | Value |
|---|---|
| **Name** | CócStudy — AI-Based Study Partner Matching System |
| **Tagline** | Học cùng nhau, tiến xa hơn mỗi ngày |
| **Type** | Fullstack SPA + REST API + WebSocket |
| **Users** | Vietnamese university students |
| **UI Language** | Vietnamese labels, English code |
| **MVP Core** | KNN-based study partner matching + real-time chat |
| **Demo credentials** | `demo@cocstudy.vn` / `demo1234` |

---

## 2. TECH STACK

| Layer | Technology |
|---|---|
| **Frontend** | React 18 + TypeScript + TailwindCSS + Framer Motion |
| **State** | Redux Toolkit + React Query (TanStack) |
| **HTTP client** | Axios with JWT interceptors |
| **Backend** | FastAPI (Python 3.11) + Uvicorn ASGI |
| **ORM** | SQLAlchemy 2 async |
| **DB** | PostgreSQL 15 |
| **Migrations** | Alembic |
| **Auth** | JWT (python-jose) + bcrypt (passlib) |
| **AI** | scikit-learn KNN + cosine similarity (numpy) |
| **Cache/PubSub** | Redis 7 (planned — not yet wired) |
| **File storage** | Local disk (StaticFiles via FastAPI) |
| **Realtime** | FastAPI WebSocket (native) |
| **Containerisation** | Docker + Docker Compose (not yet written) |

---

## 3. COMPLETE FOLDER STRUCTURE

```
cocstudy/
├── .env.example                          ✅ done
├── docker-compose.yml                    ❌ missing
├── README.md                             ❌ missing
│
├── backend/
│   ├── requirements.txt                  ✅ done
│   ├── Dockerfile                        ❌ missing
│   ├── alembic/
│   │   ├── alembic.ini                   ✅ done
│   │   ├── env.py                        ✅ done
│   │   └── versions/
│   │       └── 0001_initial_schema.py    ✅ done (12 tables)
│   ├── app/
│   │   ├── main.py                       ✅ done
│   │   ├── api/v1/
│   │   │   ├── __init__.py               ❌ missing (empty barrel)
│   │   │   ├── auth.py                   ✅ done
│   │   │   ├── users.py                  ✅ done
│   │   │   ├── profiles.py               ✅ done
│   │   │   ├── matching.py               ✅ done
│   │   │   ├── groups.py                 ✅ done
│   │   │   ├── messages.py               ✅ done (REST + WebSocket)
│   │   │   ├── notifications.py          ✅ done
│   │   │   └── uploads.py               ✅ done
│   │   ├── core/
│   │   │   ├── config.py                 ✅ done (pydantic-settings)
│   │   │   ├── security.py              ✅ done (JWT + bcrypt)
│   │   │   └── dependencies.py          ✅ done (get_db, get_current_user)
│   │   ├── models/
│   │   │   ├── __init__.py               ❌ missing
│   │   │   ├── user.py                   ✅ done
│   │   │   ├── profile.py                ✅ done
│   │   │   ├── subject.py                ✅ done (Subject + UserSubject)
│   │   │   ├── schedule.py               ✅ done
│   │   │   ├── match.py                  ✅ done
│   │   │   ├── group.py                  ✅ done (StudyGroup + GroupMember)
│   │   │   ├── message.py                ✅ done (Conversation + Message)
│   │   │   ├── notification.py           ✅ done
│   │   │   └── feedback.py               ✅ done
│   │   ├── schemas/
│   │   │   ├── auth.py                   ✅ done
│   │   │   ├── user.py                   ✅ done
│   │   │   ├── profile.py                ✅ done
│   │   │   ├── matching.py               ✅ done
│   │   │   ├── group.py                  ✅ done
│   │   │   └── message.py                ✅ done
│   │   ├── services/
│   │   │   ├── auth_service.py           ✅ done
│   │   │   ├── matching_service.py       ✅ done (KNN wiring)
│   │   │   ├── notification_service.py   ✅ done
│   │   │   ├── user_service.py           ❌ missing
│   │   │   └── group_service.py          ❌ missing
│   │   ├── ai/
│   │   │   ├── feature_builder.py        ✅ done (105-dim vectors)
│   │   │   ├── preprocessor.py           ✅ done (StandardScaler)
│   │   │   ├── recommender.py            ✅ done (KNN + weighted scoring)
│   │   │   └── two_tower/README.md       ✅ done (stub)
│   │   ├── database/
│   │   │   ├── base.py                   ✅ done
│   │   │   └── session.py                ✅ done (async engine)
│   │   ├── middleware/
│   │   │   ├── rate_limiter.py           ✅ done (sliding window)
│   │   │   └── logger.py                 ❌ missing
│   │   └── utils/
│   │       ├── file_handler.py           ❌ missing
│   │       └── validators.py             ❌ missing
│   └── tests/
│       ├── test_auth.py                  ❌ missing
│       ├── test_matching.py              ❌ missing
│       └── test_groups.py                ❌ missing
│
├── database/
│   ├── schema.sql                        ❌ missing
│   ├── seed_data.sql                     ❌ missing
│   └── erd_description.md               ❌ missing
│
├── scripts/
│   ├── seed_db.py                        ❌ missing
│   └── generate_fake_users.py            ❌ missing
│
├── docs/
│   ├── API.md                            ❌ missing
│   ├── ARCHITECTURE.md                   ❌ missing
│   └── AI_ENGINE.md                      ❌ missing
│
├── frontend/                             ❌ entirely missing (TS codebase)
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── index.html
│   └── src/
│       ├── types/index.ts
│       ├── animations/variants.ts
│       ├── services/{api, auth, matching, groups, messages}.service.ts
│       ├── store/{authSlice, matchSlice, notifSlice}.ts
│       ├── hooks/{useAuth, useMatches, useWebSocket, useProfile}.ts
│       ├── components/** (all UI components)
│       └── pages/** (all page components)
│
└── uploads/                              ✅ directories created
    ├── avatars/
    └── documents/
```

---

## 4. DATABASE SCHEMA (12 tables — all migrated in 0001)

| Table | Key Columns | Relations |
|---|---|---|
| `users` | id(UUID PK), email(unique), password_hash, full_name, university, major, gpa, role, is_active | parent of everything |
| `profiles` | id, user_id(FK unique), avatar_url, bio, learning_style, academic_goal, availability, xp_points, streak_days | 1:1 with users |
| `subjects` | id, name(unique), category, code | standalone vocab |
| `user_subjects` | (user_id, subject_id) PK, skill_level, is_seeking | M:N users↔subjects |
| `schedules` | id, user_id(FK), day_of_week(0-6), time_slot | M:1 with users |
| `matches` | id, user_id_a, user_id_b, score, subject/schedule/style/goal/gpa_score, status, initiated_by | self-join users |
| `study_groups` | id, name, description, icon, subject_id, owner_id, max_members, next_session | owned by user |
| `group_members` | (group_id, user_id) PK, role, joined_at | M:N users↔groups |
| `conversations` | id, user_id_a, user_id_b (unique pair) | 1:1 pair of users |
| `messages` | id, conversation_id(FK), sender_id, content, message_type, is_read | M:1 conversation |
| `notifications` | id, user_id(FK), type, title, body, data(JSONB), is_read | M:1 users |
| `feedback` | id, reviewer_id, reviewee_id, match_id, rating(1-5), comment | M:1 users+matches |

---

## 5. AI ENGINE SUMMARY

### Feature Vector: 105 dimensions
```
[0:50]   subject multi-hot     (50 subject vocab)
[50:92]  schedule binary       (7 days × 6 slots = 42)
[92:98]  learning_style 1-hot  (6 styles)
[98:104] academic_goal 1-hot   (6 goals)
[104]    GPA normalised        (÷ 4.0)
```

### Weights
```python
WEIGHTS = {"subjects": 0.35, "schedule": 0.25,
           "learning_style": 0.15, "academic_goal": 0.15, "gpa": 0.10}
```

### Pipeline
1. `feature_builder.py` → builds 105-dim float32 vectors from DB data
2. `preprocessor.py` → StandardScaler normalisation
3. `recommender.py` → NearestNeighbors(cosine) → top-K candidates → weighted rescore → MatchScore list
4. `matching_service.py` → DB I/O + schema translation

### Module singleton
`recommender = StudyMatchRecommender()` at module level in `recommender.py`.
`matching_service.rebuild_index(db)` triggers `recommender.fit()`.

---

## 6. IMPLEMENTED API ROUTES

### Auth — `/api/v1/auth`
| Method | Path | Done |
|---|---|---|
| POST | `/register` | ✅ |
| POST | `/login` | ✅ |
| POST | `/refresh` | ✅ |
| POST | `/logout` | ✅ |
| GET | `/me` | ✅ |

### Users — `/api/v1/users`
| Method | Path | Done |
|---|---|---|
| GET | `/me` | ✅ |
| PATCH | `/me` | ✅ |
| GET | `/search` | ✅ |
| GET | `/{user_id}` | ✅ |

### Profiles — `/api/v1/profiles`
| Method | Path | Done |
|---|---|---|
| GET | `/me` | ✅ |
| PUT | `/me` (subjects + schedule included) | ✅ |
| GET | `/{user_id}` | ✅ |

### Matching — `/api/v1/matching`
| Method | Path | Done |
|---|---|---|
| GET | `/recommendations` | ✅ |
| GET | `/score/{target_user_id}` | ✅ |
| POST | `/connect/{target_user_id}` | ✅ |
| GET | `/connections` | ✅ |

### Groups — `/api/v1/groups`
| Method | Path | Done |
|---|---|---|
| GET | `/` | ✅ |
| POST | `/` | ✅ |
| GET | `/{id}` | ✅ |
| POST | `/{id}/join` | ✅ |
| DELETE | `/{id}/leave` | ✅ |
| GET | `/{id}/members` | ✅ |

### Messages — `/api/v1/messages`
| Method | Path | Done |
|---|---|---|
| GET | `/conversations` | ✅ |
| GET | `/conversations/{id}` | ✅ |
| POST | `/conversations/{id}` | ✅ |
| WS | `/ws/{conversation_id}?token=` | ✅ |

### Notifications — `/api/v1/notifications`
| Method | Path | Done |
|---|---|---|
| GET | `/` | ✅ |
| PATCH | `/read-all` | ✅ |
| PATCH | `/{id}/read` | ✅ |

### Uploads — `/api/v1/uploads`
| Method | Path | Done |
|---|---|---|
| POST | `/avatar` | ✅ |

---

## 7. IMPLEMENTED FEATURES

### Backend
- [x] Pydantic-settings config with `.env` loading
- [x] Async SQLAlchemy engine + session factory
- [x] bcrypt password hashing
- [x] JWT access + refresh token flow
- [x] Bearer token dependency injection (`get_current_user`)
- [x] Sliding-window rate limiter middleware
- [x] CORS middleware with configurable origins
- [x] StaticFiles mount for avatar serving
- [x] Full CRUD for users, profiles, groups, notifications
- [x] WebSocket real-time chat with in-memory connection manager
- [x] Avatar upload with content-type + size validation
- [x] Alembic migration (all 12 tables)
- [x] KNN recommender with 105-dim feature vectors
- [x] Weighted multi-factor scoring (5 factors)
- [x] Subject Jaccard similarity
- [x] Schedule slot overlap scoring
- [x] GPA proximity scoring
- [x] Lifespan event: auto-create tables in dev, dispose engine on shutdown

### Frontend (browser prototype only — TS codebase not started)
- [x] Landing page with hero, stats, how-it-works
- [x] Login / register forms
- [x] 4-step onboarding wizard (subjects, style, goal, schedule grid)
- [x] Discover page with AI match cards + animated AI Match button
- [x] Compatibility detail page with factor bars
- [x] Study groups page with join/leave
- [x] Chat UI with multi-conversation support + real send
- [x] Notifications page
- [x] Profile page with stats + skills
- [x] Settings page

---

## 8. CODING CONVENTIONS

### Python
- Black formatter, line length 88
- Type hints on all signatures
- Google-style docstrings on all service/AI functions
- HTTPException with `{"code": "SCREAMING_SNAKE", "message": "..."}` detail
- `structlog` for JSON logging
- Async everywhere (SQLAlchemy async, aiofiles, httpx)
- Model naming: singular PascalCase (`User`, `Match`, `StudyGroup`)
- File naming: snake_case

### Database
- UUIDs (`gen_random_uuid()`) for all PKs
- `created_at` + `updated_at` on all tables
- `is_active` soft-delete on users
- Indexes on all FK columns + common query columns
- Table names: plural snake_case (`study_groups`, `user_subjects`)

### TypeScript (target conventions for missing files)
- ESLint + Prettier, 2-space indent, single quotes
- React 18 functional components only
- `IUser`, `IMatch` etc. for type interfaces
- `use` prefix for all hooks
- `.service.ts` suffix for API service files
- Redux Toolkit slices in `store/`
- Axios instance in `services/api.ts` with JWT interceptor

---

## 9. ENVIRONMENT VARIABLES

All defined in `.env.example`. Key variables:
```
DATABASE_URL=postgresql+asyncpg://cocstudy:password@localhost:5432/cocstudy_db
SECRET_KEY=<32+ char random string>
ALLOWED_ORIGINS=http://localhost:5173,...
REDIS_URL=redis://localhost:6379/0
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
UPLOAD_DIR=./uploads
MAX_AVATAR_SIZE_MB=5
AI_CACHE_TTL=3600
KNN_NEIGHBORS=20
RATE_LIMIT_PER_MINUTE=60
```

---

## 10. REMAINING TASKS (priority ordered)

### 🔴 P0 — Backend completions (small, unblocking)
1. `backend/app/api/v1/__init__.py` — empty barrel file
2. `backend/app/models/__init__.py` — import all models (needed by Alembic env.py)
3. `backend/app/services/user_service.py` — user search + update helpers
4. `backend/app/services/group_service.py` — group business logic extraction
5. `backend/app/middleware/logger.py` — structlog request logger
6. `backend/app/utils/file_handler.py` — image validation helpers
7. `backend/app/utils/validators.py` — reusable input validators

### 🔴 P0 — Infrastructure
8. `backend/Dockerfile`
9. `docker-compose.yml` (backend + frontend + postgres + redis)

### 🟡 P1 — Tests
10. `backend/tests/conftest.py` — pytest fixtures (in-memory SQLite async)
11. `backend/tests/test_auth.py`
12. `backend/tests/test_matching.py`
13. `backend/tests/test_groups.py`

### 🟡 P1 — Database assets
14. `database/schema.sql` — raw DDL export
15. `database/seed_data.sql` — demo users/groups/subjects
16. `database/erd_description.md`

### 🟡 P1 — Scripts
17. `scripts/seed_db.py` — async seeder using SQLAlchemy
18. `scripts/generate_fake_users.py` — Faker-based bulk generator

### 🟡 P1 — Docs
19. `docs/API.md`
20. `docs/AI_ENGINE.md`
21. `docs/ARCHITECTURE.md`

### 🟢 P2 — Frontend TypeScript codebase
22. `frontend/package.json` + config files (vite, tailwind, tsconfig)
23. `frontend/src/types/index.ts`
24. `frontend/src/animations/variants.ts`
25. `frontend/src/services/api.ts` (Axios instance)
26. `frontend/src/services/auth.service.ts`
27. `frontend/src/services/matching.service.ts`
28. `frontend/src/services/groups.service.ts`
29. `frontend/src/services/messages.service.ts`
30. `frontend/src/store/authSlice.ts`
31. `frontend/src/store/matchSlice.ts`
32. `frontend/src/store/notifSlice.ts`
33. `frontend/src/hooks/useAuth.ts`
34. `frontend/src/hooks/useMatches.ts`
35. `frontend/src/hooks/useWebSocket.ts`
36. `frontend/src/hooks/useProfile.ts`
37. All component + page `.tsx` files
38. `frontend/Dockerfile`

### 🟢 P3 — Enhancements
39. Redis integration for AI index caching
40. Background task: periodic `rebuild_index` (APScheduler)
41. Email verification flow
42. Friend request system
43. Study session booking
44. Dark mode token set

---

## 11. NEXT DEVELOPMENT SESSION — START HERE

**Pick up from:** remaining backend completions (P0 items 1-9 above).

**Order to follow:**
```
1. __init__.py barrel files           (unblocks Alembic / imports)
2. user_service + group_service       (completes service layer)
3. middleware/logger.py               (completes middleware layer)
4. utils/                             (completes utils layer)
5. Dockerfile + docker-compose.yml    (makes project runnable)
6. tests/                             (validates correctness)
7. database/seed_data.sql             (enables local dev)
8. scripts/seed_db.py                 (runnable seeder)
9. README.md                          (project usable by new devs)
10. frontend TS codebase              (P2 — full React app)
```

**DO NOT re-write any existing ✅ files.**