# ✅ CócStudy — TODO QUEUE
> Ordered by priority. Check off as each file is completed. DO NOT skip items in a block.

---

## BLOCK A — Backend barrel files (unblock imports) 🔴 P0
- [x] `backend/app/api/v1/__init__.py` — empty, fixes import resolution
- [x] `backend/app/models/__init__.py` — re-exports all models so Alembic env.py detects them

## BLOCK B — Service layer completion 🔴 P0
- [x] `backend/app/services/user_service.py`
  - `get_user_by_id(id, db)` → User | None
  - `search_users(q, major, university, limit, db)` → list[User]
  - `update_user(user, data, db)` → User
- [x] `backend/app/services/group_service.py`
  - `get_group_with_count(id, db)` → (StudyGroup, int)
  - `user_is_member(group_id, user_id, db)` → bool
  - `get_member_count(group_id, db)` → int

## BLOCK C — Middleware + utils 🔴 P0
- [x] `backend/app/middleware/logger.py` — structlog JSON request logger
- [x] `backend/app/utils/file_handler.py` — validate_image(), get_safe_filename()
- [x] `backend/app/utils/validators.py` — validate_gpa(), validate_year(), validate_uuid()

## BLOCK D — Infrastructure 🔴 P0
- [x] `backend/Dockerfile` — multi-stage Python 3.11 slim
- [x] `docker-compose.yml` — 4 services: postgres, redis, backend, frontend

## BLOCK E — Tests 🟡 P1
- [x] `backend/tests/conftest.py` — async SQLite engine, test client fixtures
- [x] `backend/tests/test_auth.py` — register, login, refresh, protected route
- [x] `backend/tests/test_matching.py` — feature vector, KNN output, score endpoint
- [x] `backend/tests/test_groups.py` — create, join, leave, capacity limit

## BLOCK F — Database assets 🟡 P1
- [x] `database/schema.sql` — full DDL (mirrors 0001 migration)
- [x] `database/seed_data.sql` — 8 demo users, 6 groups, 16 subjects
- [x] `database/erd_description.md` — table map + relationship explanations

## BLOCK G — Scripts 🟡 P1
- [x] `scripts/seed_db.py` — async SQLAlchemy seeder (runs standalone)
- [x] `scripts/generate_fake_users.py` — Faker: bulk generate N users with profiles

## BLOCK H — Docs 🟡 P1
- [x] `docs/API.md` — all endpoints with request/response examples
- [x] `docs/AI_ENGINE.md` — feature vector, weights, pipeline, future roadmap
- [x] `docs/ARCHITECTURE.md` — system diagram + deployment topology

## BLOCK I — README 🟡 P1
- [x] `README.md` — setup, run, test, deploy instructions

## BLOCK J — Frontend TypeScript (config + foundation) 🟢 P2
- [x] `frontend/package.json`
- [x] `frontend/vite.config.ts`
- [x] `frontend/tailwind.config.ts` — CócStudy design tokens
- [x] `frontend/tsconfig.json`
- [x] `frontend/index.html`
- [x] `frontend/src/types/index.ts` — IUser, IMatch, IGroup, IMessage etc.
- [x] `frontend/src/animations/variants.ts`

## BLOCK K — Frontend services + state 🟢 P2
- [x] `frontend/src/services/api.ts` — Axios instance + JWT interceptor + refresh
- [x] `frontend/src/services/auth.service.ts`
- [x] `frontend/src/services/matching.service.ts`
- [x] `frontend/src/services/groups.service.ts`
- [x] `frontend/src/services/messages.service.ts`
- [x] `frontend/src/store/authSlice.ts`
- [x] `frontend/src/store/matchSlice.ts`
- [x] `frontend/src/store/notifSlice.ts`
- [x] `frontend/src/hooks/useAuth.ts`
- [x] `frontend/src/hooks/useMatches.ts`
- [x] `frontend/src/hooks/useWebSocket.ts`
- [x] `frontend/src/hooks/useProfile.ts`

## BLOCK L — Frontend components + pages 🟢 P2
- [x] `src/components/ui/` (Button, Card, Badge, Tag, Avatar, Input, Modal)
- [x] `src/components/layout/` (Navbar, Sidebar, MobileNav)
- [x] `src/components/matching/` (MatchCard, ScoreRing, CompatChart)
- [x] `src/components/groups/` (GroupCard, MemberAvatars)
- [x] `src/components/chat/` (ChatWindow, MessageBubble, ChatList)
- [x] `src/components/profile/` (ProfileHero, SkillGrid, StatsGrid)
- [x] `src/components/onboarding/` (WizardStep, SubjectPicker, ScheduleGrid)
- [x] `src/pages/Landing.tsx`
- [x] `src/pages/Login.tsx` + `Register.tsx`
- [x] `src/pages/Onboarding.tsx`
- [x] `src/pages/Discover.tsx`
- [x] `src/pages/Compatibility.tsx`
- [x] `src/pages/Groups.tsx`
- [x] `src/pages/Messages.tsx`
- [x] `src/pages/Notifications.tsx`
- [x] `src/pages/Profile.tsx`
- [x] `src/pages/Settings.tsx`
- [x] `frontend/Dockerfile`

## BLOCK M — P3 Enhancements (post-MVP)
- [ ] Redis wiring for AI index cache (TTL = AI_CACHE_TTL)
- [ ] APScheduler background task: rebuild_index every hour
- [ ] Email verification (SMTP via fastapi-mail)
- [ ] Friend request system (separate from match)
- [ ] Study session booking (calendar slots)
- [ ] Dark mode CSS token set
- [ ] Push notifications (Web Push API)
- [ ] Admin dashboard page

---
## Rules
1. Only mark ✅ when the file is written AND lint-clean.
2. Never modify existing ✅ backend files — only extend.
3. Each block must be fully done before starting the next.