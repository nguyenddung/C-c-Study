# 📋 CócStudy — FILE MANIFEST
> Last updated: 2026-05-25 | Legend: ✅ exists & complete · ❌ missing · 🔨 in-progress

## Root
| File | Status | Notes |
|---|---|---|
| `.env.example` | ✅ | All env vars documented |
| `docker-compose.yml` | ✅ | postgres + redis + backend + frontend |
| `README.md` | ✅ | Full setup guide |
| `PROJECT_MEMORY.md` | ✅ | This snapshot |
| `FILE_MANIFEST.md` | ✅ | This file |
| `TODO_QUEUE.md` | ✅ | Ordered task queue |

## backend/
| File | Status | Notes |
|---|---|---|
| `requirements.txt` | ✅ | All deps pinned |
| `Dockerfile` | ✅ | Multi-stage Python 3.11 |
| `alembic/alembic.ini` | ✅ | |
| `alembic/env.py` | ✅ | Async Alembic env |
| `alembic/versions/0001_initial_schema.py` | ✅ | 12 tables |
| `app/main.py` | ✅ | FastAPI app + routers + lifespan |
| `app/api/v1/__init__.py` | ✅ | Barrel |
| `app/api/v1/auth.py` | ✅ | register/login/refresh/logout/me |
| `app/api/v1/users.py` | ✅ | me/search/{id} |
| `app/api/v1/profiles.py` | ✅ | get+put profile |
| `app/api/v1/matching.py` | ✅ | recommendations/score/connect |
| `app/api/v1/groups.py` | ✅ | CRUD + join/leave/members |
| `app/api/v1/messages.py` | ✅ | REST + WebSocket |
| `app/api/v1/notifications.py` | ✅ | list/read-all/read |
| `app/api/v1/uploads.py` | ✅ | avatar upload |
| `app/core/config.py` | ✅ | pydantic-settings |
| `app/core/security.py` | ✅ | JWT + bcrypt |
| `app/core/dependencies.py` | ✅ | get_db + get_current_user |
| `app/models/__init__.py` | ✅ | Imports all models |
| `app/models/user.py` | ✅ | |
| `app/models/profile.py` | ✅ | |
| `app/models/subject.py` | ✅ | Subject + UserSubject |
| `app/models/schedule.py` | ✅ | |
| `app/models/match.py` | ✅ | |
| `app/models/group.py` | ✅ | StudyGroup + GroupMember |
| `app/models/message.py` | ✅ | Conversation + Message |
| `app/models/notification.py` | ✅ | |
| `app/models/feedback.py` | ✅ | |
| `app/schemas/auth.py` | ✅ | |
| `app/schemas/user.py` | ✅ | |
| `app/schemas/profile.py` | ✅ | |
| `app/schemas/matching.py` | ✅ | |
| `app/schemas/group.py` | ✅ | |
| `app/schemas/message.py` | ✅ | |
| `app/services/auth_service.py` | ✅ | register/login/refresh |
| `app/services/matching_service.py` | ✅ | DB→AI wiring |
| `app/services/notification_service.py` | ✅ | create helper |
| `app/services/user_service.py` | ✅ | search + update |
| `app/services/group_service.py` | ✅ | business logic |
| `app/ai/feature_builder.py` | ✅ | 105-dim vectors |
| `app/ai/preprocessor.py` | ✅ | StandardScaler |
| `app/ai/recommender.py` | ✅ | KNN + weighted score |
| `app/ai/two_tower/README.md` | ✅ | Future stub |
| `app/database/base.py` | ✅ | DeclarativeBase |
| `app/database/session.py` | ✅ | async engine |
| `app/middleware/rate_limiter.py` | ✅ | sliding window |
| `app/middleware/logger.py` | ✅ | structlog middleware |
| `app/utils/file_handler.py` | ✅ | image validation |
| `app/utils/validators.py` | ✅ | reusable validators |
| `tests/conftest.py` | ✅ | pytest async fixtures |
| `tests/test_auth.py` | ✅ | auth endpoint tests |
| `tests/test_matching.py` | ✅ | AI + matching tests |
| `tests/test_groups.py` | ✅ | group CRUD tests |

## database/
| File | Status | Notes |
|---|---|---|
| `schema.sql` | ✅ | Raw DDL |
| `seed_data.sql` | ✅ | Demo data |
| `erd_description.md` | ✅ | ERD + relationships |

## scripts/
| File | Status | Notes |
|---|---|---|
| `seed_db.py` | ✅ | Async SQLAlchemy seeder |
| `generate_fake_users.py` | ✅ | Faker bulk generator |

## docs/
| File | Status | Notes |
|---|---|---|
| `API.md` | ✅ | Full endpoint reference |
| `AI_ENGINE.md` | ✅ | Algorithm documentation |
| `ARCHITECTURE.md` | ✅ | System design |

## frontend/
| File | Status | Notes |
|---|---|---|
| `package.json` | ✅ | React 18 + TS + Vite |
| `vite.config.ts` | ✅ | |
| `tailwind.config.ts` | ✅ | CócStudy design tokens |
| `tsconfig.json` | ✅ | |
| `index.html` | ✅ | |
| `Dockerfile` | ✅ | Nginx static build |
| `src/types/index.ts` | ✅ | All shared interfaces |
| `src/animations/variants.ts` | ✅ | Framer Motion variants |
| `src/services/api.ts` | ✅ | Axios + JWT interceptor |
| `src/services/auth.service.ts` | ✅ | |
| `src/services/matching.service.ts` | ✅ | |
| `src/services/groups.service.ts` | ✅ | |
| `src/services/messages.service.ts` | ✅ | |
| `src/store/authSlice.ts` | ✅ | Redux Toolkit |
| `src/store/matchSlice.ts` | ✅ | |
| `src/store/notifSlice.ts` | ✅ | |
| `src/hooks/useAuth.ts` | ✅ | |
| `src/hooks/useMatches.ts` | ✅ | |
| `src/hooks/useWebSocket.ts` | ✅ | |
| `src/hooks/useProfile.ts` | ✅ | |
| `src/components/ui/*` | ✅ | Button, Card, Badge, Tag, Avatar, Input |
| `src/components/layout/*` | ✅ | Navbar, Sidebar, MobileNav |
| `src/components/matching/*` | ✅ | MatchCard, CompatChart, ScoreRing |
| `src/components/groups/*` | ✅ | GroupCard, MemberAvatars |
| `src/components/chat/*` | ✅ | ChatWindow, MessageBubble |
| `src/components/profile/*` | ✅ | ProfileHero, SkillGrid |
| `src/components/onboarding/*` | ✅ | WizardStep, SubjectPicker, ScheduleGrid |
| `src/pages/Landing.tsx` | ✅ | |
| `src/pages/Login.tsx` | ✅ | |
| `src/pages/Register.tsx` | ✅ | |
| `src/pages/Onboarding.tsx` | ✅ | |
| `src/pages/Discover.tsx` | ✅ | |
| `src/pages/Compatibility.tsx` | ✅ | |
| `src/pages/Groups.tsx` | ✅ | |
| `src/pages/Messages.tsx` | ✅ | |
| `src/pages/Notifications.tsx` | ✅ | |
| `src/pages/Profile.tsx` | ✅ | |
| `src/pages/Settings.tsx` | ✅ | |