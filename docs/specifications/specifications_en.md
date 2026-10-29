# Specifications

## _PandaDev Portfolio_

> 🇫🇷 Version française : [specifications_fr.md](specifications_fr.md)

| Version     | Date       | Authors                        | Changes       |
|-------------|------------|--------------------------------|---------------|
| 0.1 (draft) | 2026-10-29 | Mathieu MORIN, Mathias GARAIOS | First version |

---

## 1. Context

### 1.1 Project overview

PandaDev is a team of developers. The project is a website that brings several portfolios together: each member presents their profile, skills, background and projects there, and the projects built together are shown once, with the role of each member. The website is not limited to a fixed number of portfolios (see [3.5 Adding a portfolio](#35-adding-a-portfolio)).

### 1.2 Roles in the project

The team members are at the same time the clients, the developers and the users of the website. They share:

- the design (specifications, database schema);
- the development of the API, the website and the database;
- the documentation;
- entering their own content in the private area.

### 1.3 Target audience

- Recruiters and companies, especially for internship, apprenticeship or job offers;
- Teachers, juries and other developers who want to see real work.

### 1.4 Problem

A résumé or a LinkedIn profile does not show the projects themselves: the code, the screenshots, the technologies used, the role of each member in a group project. The members want:

- a single website that presents the team while letting each member keep their own identity;
- content they can edit from a private area, without touching the code or redeploying the website (only the layout specific to each member is done in the code, see [3.5](#35-adding-a-portfolio));
- a bilingual website, in French and English.

### 1.5 Chosen solution

Three components, versioned in the same repository:

- **REST API (FastAPI, Python 3.15, SQLModel)**: login and password authentication (JWT token), public reading of the content, writing restricted to logged-in members, image upload.
- **Website (Nuxt 4, Nuxt UI, Bun)**: public part (home, portfolios, projects, about) and private area to enter the content. Translation with `@nuxtjs/i18n`.
- **Database (PostgreSQL 18, Docker Compose)**: stores the content (profiles, projects, technologies, media…). Image files are stored outside the database. The schema is described in [`docs/database/`](../database/).

---

## 2. Current state

### 2.1 Already done

| Item           | Detail                                                                                                                                                          |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Authentication | Login and password (bcrypt, JWT token), sealed Nuxt session, logout                                                                                             |
| Private area   | "My area" page restricted to logged-in members, still empty                                                                                                     |
| Translation    | Interface fully translated into French (default locale) and English                                                                                             |
| Look and feel  | PandaDev color palette (Radix), light / dark mode, responsive header                                                                                            |
| Public pages   | Home, Projects and About pages created, without content                                                                                                         |
| Portfolios     | One page per member, with the structure of its own layout (layout, header, hero) and shared components (projects, background, technologies, links), still empty |
| Database       | `users` table created; full schema proposed ([schema.puml](../database/schema.puml), [data dictionary](../database/data_dictionary.md))                         |

### 2.2 Still to do

- Create the tables of the proposed schema and the matching API routes;
- Show the content on the public pages;
- Build the forms of the private area;
- Set up image storage;
- Create the website footer, shown on every page, with the link to the legal notice;
- Choose the host, needed to go live and for the "Legal notice" page.

---

## 3. Functional requirements

### 3.1 Essential features

1. Present the portfolio of each member: profile, availability, skills, background and links.
2. Present the projects, individual or group ones, with the role of each member.
3. Let each member edit their content from the private area, without touching the code.
4. Offer all the content in French and English.

### 3.2 User actions

A visitor can:

- view the home page, the portfolios, the projects and the About page;
- go from one portfolio to another from the navigation bar;
- filter the projects by technology or by member;
- switch the language and switch between light and dark mode;
- contact a member by email, by phone or through their links (LinkedIn, Discord…), when the member has set them.

A logged-in member can:

- edit their profile, their contact details, their availability and their "Now" section;
- manage their links, their background and their technologies;
- create, edit, publish and feature the projects they are a member of;
- add co-authors to a project and set their role;
- upload images (avatar, cover, gallery).

### 3.3 Data to store

The detail of each field (type, constraints, required or not) is in the [data dictionary](../database/data_dictionary.md). In short:

| Data         | Content                                                                                                                            |
|--------------|------------------------------------------------------------------------------------------------------------------------------------|
| Profile      | Display name, headline, bio, city, avatar, availability, "Now" section, contact email and phone, CV in PDF per language (optional) |
| Links        | GitHub, Discord, YouTube, LinkedIn, all optional                                                                                   |
| Background   | Work experiences and education                                                                                                     |
| Technologies | Shared catalog (name, category, icon); score from 0 to 100 per member, level computed automatically                                |
| Projects     | Title, summary, presentation, cover, gallery, links, dates, technologies, members and roles, draft or published, featured          |
| Media        | Images (WebP) and PDF: dimensions, size, alternative text                                                                          |

Every text shown to visitors is entered in both languages.

### 3.4 Expected results

- In less than a minute, a visitor understands who each member is, what they can do and whether they are available.
- Each group project clearly shows who did what.
- A member updates their content in a few minutes, without help and without redeploying.
- A draft is never visible to the public.

### 3.5 Adding a portfolio

The website is not limited to a fixed number of portfolios. The **content** of a portfolio is managed from the private area; its **own layout** is done in the code.

Adding a member takes three steps:

1. **Account**: a developer creates the member's account in the database and picks their slug, e.g. `jean-dupont`.
2. **Content**: the member logs in and fills in their profile, links, background and technologies from the private area. Their portfolio is then visible at `/portfolios/<slug>`, with the default layout.
3. **Own layout (optional)**: a developer creates, in `web/app/`:
   - `pages/portfolios/<slug>/index.vue`: the member's page;
   - `layouts/<slug>.vue`: their layout;
   - `components/<slug>/`: their components (header, hero…), which can reuse the shared components of `components/portfolio/`.

   This page automatically replaces the default page for this member.

Files are named after the slug, which is unique, so two people with the same name cannot clash (two "Jean Dupont" would get, for example, the slugs `jean-dupont` and `jean-dupont-2`).

---

## 4. Non-functional requirements

| Criterion       | Detail                                                                                                                                                                                                                                                                                                       |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Languages       | Interface and content in French (default) and English; content without both translations is rejected                                                                                                                                                                                                         |
| Responsive      | Usable on desktop, tablet and phone                                                                                                                                                                                                                                                                          |
| Accessibility   | Alternative text required on images, contrast of the Radix palette, keyboard navigation                                                                                                                                                                                                                      |
| Security        | Strong (see UC-12) and hashed (bcrypt) passwords, JWT tokens, writing restricted to logged-in members, project editing restricted to its members                                                                                                                                                             |
| Errors          | 404 and error pages in the website style, translated, with the header and a link back to the home page; no technical detail is shown to the visitor                                                                                                                                                          |
| Legal notice    | "Legal notice" page (website publishers, host), translated and reachable from the footer of every page                                                                                                                                                                                                       |
| Files           | Real file type checked, size limited, conversion to WebP, EXIF data removed, random file name                                                                                                                                                                                                                |
| Backups         | Automatic daily backup of the database and of the `uploads/` folder, kept for 30 days; a restore is tested before going live                                                                                                                                                                                 |
| Performance     | Optimized images (WebP), Nuxt server-side rendering for a fast first display                                                                                                                                                                                                                                 |
| SEO             | Server-side rendering, readable URLs (slugs), title and description specific to each page, share preview (Open Graph) with the member's avatar or the project cover, `sitemap.xml` of the public pages (no drafts, no private area), links between the French and English versions of each page (`hreflang`) |
| Maintainability | Typed code, linters (ruff, ESLint), API tests (pytest) and website tests (Vitest with `@nuxt/test-utils` for components, Playwright for the main flows: login, viewing a portfolio, publishing a project), documentation kept up to date                                                                     |

---

## 5. Constraints and limits

- **Accounts**: no public sign-up. Member accounts are created directly in the database, with their slug. A slug can still be changed in the database, but the member's layout files must then be renamed, and old links stop working. Accounts are deleted in the database as well.
- **Languages**: French and English only.
- **Contact**: no contact form, so no messages to store and no spam to handle. Visitors email or call the member directly, or use their links.
- **Links**: limited to GitHub, Discord, YouTube and LinkedIn. Adding another one requires a database migration.
- **Privacy**: no personal data of visitors is collected. Only the information the members choose to publish is stored, including their contact email and phone, which stay optional. The IP address of a visitor is only used, in memory, to limit the requests for contact details and CVs; it is never stored. The website only uses technical cookies and local storage (login session, language, light / dark mode and theme): no consent banner is needed.
- **Hosting**: to be decided. The choice must be made before going live, because the "Legal notice" page must give the name, address and phone number of the host.

---

## 6. Personas

### The recruiter visitor

Browses the portfolios and the projects.

| Attribute       | Detail                                                                                   |
|-----------------|------------------------------------------------------------------------------------------|
| Profile         | Recruiter, HR officer, apprenticeship tutor or teacher                                   |
| Main goal       | Quickly assess the skills and availability of a member                                   |
| Behavior        | Short visit, often on a phone: looks at the featured projects, then one or two in detail |
| Technical level | Varies: the website must stay readable without technical knowledge                       |
| Expectations    | Know who did what, see real work (screenshots, code, demo), find a way to get in touch   |

### The PandaDev member

Manages their portfolio and projects from the private area.

| Attribute       | Detail                                                                                    |
|-----------------|-------------------------------------------------------------------------------------------|
| Profile         | Developer, member of the PandaDev team                                                    |
| Main goal       | Present their skills and projects, keep their portfolio up to date                        |
| Behavior        | Logs in from time to time to add a project or a technology, or update their "Now" section |
| Technical level | Developer, but entering content must stay quick and never require touching the database   |
| Rights          | Edits their own profile and the projects they are a member of                             |

---

## 7. Use cases

Status: ✅ done, 🟡 started, ⬜ to do.

| #     | Use case                        | Actor           | Status |
|-------|---------------------------------|-----------------|--------|
| UC-01 | View the home page              | Visitor         | 🟡     |
| UC-02 | Browse the portfolios           | Visitor         | ⬜     |
| UC-03 | View the portfolio of a member  | Visitor         | 🟡     |
| UC-04 | Browse the projects             | Visitor         | 🟡     |
| UC-05 | View a project                  | Visitor         | ⬜     |
| UC-06 | View the About page             | Visitor         | 🟡     |
| UC-07 | Customize the display           | Visitor         | 🟡     |
| UC-08 | Search the website              | Visitor         | ⬜     |
| UC-09 | View the timeline               | Visitor         | ⬜     |
| UC-10 | View the statistics             | Visitor         | ⬜     |
| UC-11 | Find the easter egg             | Visitor         | ⬜     |
| UC-12 | Log in and log out              | Member          | 🟡     |
| UC-13 | Edit one's profile              | Member          | ⬜     |
| UC-14 | Manage one's social links       | Member          | ⬜     |
| UC-15 | Manage one's background         | Member          | ⬜     |
| UC-16 | Manage one's technologies       | Member          | ⬜     |
| UC-17 | Manage the technology catalog   | Member          | ⬜     |
| UC-18 | Manage a project                | Member          | ⬜     |
| UC-19 | Manage the members of a project | Member          | ⬜     |
| UC-20 | Upload and manage media         | Member          | ⬜     |
| UC-21 | Write and read recommendations  | Member, visitor | ⬜     |
| UC-22 | Publish and read the devlog     | Member, visitor | ⬜     |

---

## 8. User stories

Each use case groups its user stories, written as "As a…, I want…, so that…", followed by its acceptance criteria.

### UC-01 — View the home page

- **US-01.1** — As a visitor, I want to see the featured projects on the home page, so that I discover the best work of the team without searching.
- **US-01.2** — As a visitor, I want to see the team members with their headline and availability, so that I quickly know whom to contact.

Acceptance criteria:

- only published and featured projects are shown, sorted by position;
- each member links to their portfolio.

### UC-02 — Browse the portfolios

- **US-02.1** — As a visitor, I want to see the list of members (picture, name, headline, availability), so that I choose which portfolio to view.
- **US-02.2** — As a visitor, I want to reach each portfolio from the navigation bar, so that I go from one member to another without going back to the home page.

Acceptance criteria:

- the "Portfolios" entry of the header opens a menu that lists each portfolio, with an "All portfolios" link to the list page;
- this menu is built from the stored profiles, with no list written in the code, and it is present in every header (main website and portfolios);
- the current portfolio is highlighted in the menu;
- the menu stays usable on mobile, in the side panel;
- a member without a profile appears neither on the page nor in the menu.

### UC-03 — View the portfolio of a member

- **US-03.1** — As a visitor, I want to read the presentation of a member (bio, city, availability), so that I know who they are and whether they are looking for an internship, an apprenticeship or a job.
- **US-03.2** — As a visitor, I want to see their technologies grouped by category with their level, so that I can assess their skills.
- **US-03.3** — As a visitor, I want to see their background (experiences and education), from the most recent, so that I understand how they progressed.
- **US-03.4** — As a visitor, I want to see their projects and their "Now" section, so that I know what they built and what they are working on right now.
- **US-03.5** — As a member, I want my portfolio to have its own layout, so that it reflects my personality.
- **US-03.6** — As a visitor, I want to download the CV of a member, so that I can add it to a recruitment file.

Acceptance criteria:

- the address is `/portfolios/<slug>` (`/en/portfolios/<slug>` in English);
- the availability is shown as a badge, and is hidden when not set;
- the "Now" section shows the date of its last update;
- only the links that are set are shown;
- the CV download button is shown only when a CV exists; it offers the CV in the active language, or the other one when only one exists;
- the email and phone are shown only when set;
- the email, the phone and the CV link are not included in the page sent to the browser: the visitor clicks "Show email", "Show phone" or "Download CV", and the website then requests them from the API, so that spam bots cannot easily collect them (a CV usually contains the same contact details);
- the API limits the number of these requests per visitor (e.g. 10 per minute), so that a bot cannot collect them in bulk.

### UC-04 — Browse the projects

- **US-04.1** — As a visitor, I want to see every published project as a card (cover, title, summary, technologies), so that I get an overview.
- **US-04.2** — As a visitor, I want to filter the projects by technology or by member, so that I find the ones I am interested in.

Acceptance criteria:

- drafts are never shown;
- projects are sorted by position, then from the most recent;
- filters can be combined.

### UC-05 — View a project

- **US-05.1** — As a visitor, I want to read the full presentation of a project and see its image gallery, so that I understand what it does.
- **US-05.2** — As a visitor, I want to see the members of the project and the role of each one, so that I know who did what.
- **US-05.3** — As a visitor, I want to open the code repository and the demo, so that I can judge the actual work.

Acceptance criteria:

- the address is `/projects/<slug>`;
- a draft returns a 404 page to a visitor;
- a missing repository or demo link is not shown;
- a project without an end date is shown as "ongoing".

### UC-06 — View the About page

- **US-06.1** — As a visitor, I want to read a presentation of the PandaDev team, so that I understand what brings its members together and how they work.

Acceptance criteria:

- the text is a fixed text of the website, translated in the locale files, not stored in the database.

### UC-07 — Customize the display

- **US-07.1** ✅ — As a visitor, I want to switch the language of the website, so that I read it in French or English.
- **US-07.2** ✅ — As a visitor, I want to switch between light and dark mode, so that I read comfortably.
- **US-07.3** — As a visitor, I want to pick a color theme inspired by a code editor, so that I enjoy a developer touch.

Acceptance criteria:

- the language is part of the address (`/en/…` for English);
- the chosen mode and theme are remembered for the next visit;
- every theme meets the minimum accessibility contrast.

### UC-08 — Search the website

- **US-08.1** — As a visitor, I want to open a search with Ctrl+K (⌘K on Mac) and find a project, a technology or a member, so that I go straight to what interests me.

Acceptance criteria:

- results are in the active language;
- drafts are excluded;
- the search can be used with the keyboard only.

### UC-09 — View the timeline

- **US-09.1** — As a visitor, I want to see the projects and the background of the members on a timeline, so that I follow how the team progressed.

Acceptance criteria:

- the timeline is built from the dates already stored, without extra data;
- it can be filtered by member.

### UC-10 — View the statistics

- **US-10.1** — As a visitor, I want to see team statistics (number of projects, most used technologies…), so that I measure its activity.
- **US-10.2** — As a visitor, I want to see the GitHub statistics of a project (stars, commits, languages), so that I judge its activity.

Acceptance criteria:

- team statistics are computed from the existing data;
- GitHub statistics are read from the GitHub API using the repository link, cached, and never stored in the database;
- if GitHub does not answer, the block is hidden without error.

### UC-11 — Find the easter egg

- **US-11.1** — As a curious visitor, I want to find a hidden surprise (for example with the Konami code), so that browsing the website makes me smile.

Acceptance criteria:

- the surprise never gets in the way of normal browsing;
- it neither collects nor stores any data.

### UC-12 — Log in and log out

- **US-12.1** ✅ — As a member, I want to log in with my login and password, so that I reach my private area.
- **US-12.2** ✅ — As a member, I want to log out, so that I protect my account on a shared computer.
- **US-12.3** — As a member, I want to change my password from my private area, so that I never depend on a change in the database.

Acceptance criteria:

- a translated error message is shown when the credentials are wrong;
- the private area redirects to the login page when the member is not logged in;
- the current password is required to set a new one;
- the new password is entered twice and is at least 12 characters long (at most 72 bytes, the bcrypt limit);
- it gets a strength score of at least 3 out of 4 (zxcvbn library): common words, dates, keyboard sequences, the login and the member's name are rejected;
- a meter shows the password strength while typing;
- these rules are checked by the API, not only by the website;
- after the change, every other session is logged out (the API rejects the tokens issued before the change date); the current session gets a new token and stays logged in;
- a translated confirmation message is shown after the change.

### UC-13 — Edit one's profile

- **US-13.1** — As a member, I want to edit my display name, headline, bio and city, so that my presentation stays up to date.
- **US-13.2** — As a member, I want to change my profile picture, so that people recognize me.
- **US-13.3** — As a member, I want to set my availability (open to work, looking for an internship, looking for an apprenticeship, not available), so that recruiters know whether I am available.
- **US-13.4** — As a member, I want to update my "Now" section, so that I show what I am working on right now.
- **US-13.5** — As a member, I want to set a contact email and phone number, so that recruiters can reach me directly.
- **US-13.6** — As a member, I want to upload my CV in PDF, in French and in English, so that recruiters can download it.

Acceptance criteria:

- texts are entered in French and English;
- the URL identifier (slug) is unique and only contains lowercase letters, digits and dashes;
- the slug is picked when the account is created (see [3.5](#35-adding-a-portfolio)) and cannot be changed from the private area, because it sets the portfolio address and the names of its layout files;
- the update date of "Now" changes automatically each time the section is edited;
- the email and phone are optional; an invalid address is rejected and the number is stored in international format (`+33…`);
- each CV (French, English) is optional; only a PDF is accepted (10 MB at most, see UC-20), and the API checks that the linked file is a PDF;
- replacing a CV deletes the old file;
- a member can only edit their own profile.

### UC-14 — Manage one's social links

- **US-14.1** — As a member, I want to add, edit or delete my GitHub, Discord, YouTube and LinkedIn links, so that visitors can contact me or see my activity.
- **US-14.2** — As a member, I want to choose the order of my links, so that the most important one comes first.

Acceptance criteria:

- every link is optional, with at most one link per network;
- an invalid address is rejected.

### UC-15 — Manage one's background

- **US-15.1** — As a member, I want to add, edit or delete a work experience or an education entry, so that I present my background.

Acceptance criteria:

- the end date is optional (ongoing entry) and cannot be before the start date;
- a deletion asks for confirmation.

### UC-16 — Manage one's technologies

- **US-16.1** — As a member, I want to add a technology from the catalog to my profile with a score from 0 to 100, so that I show my level.
- **US-16.2** — As a member, I want to see the level computed from my score (Beginner, Intermediate, Advanced, Expert), so that I know how it will be shown.
- **US-16.3** — As a member, I want to choose the order of my technologies, so that the main ones come first.

Acceptance criteria:

- the level is computed by the database and cannot be entered;
- a technology can only be added once per member;
- a score outside 0 to 100 is rejected.

### UC-17 — Manage the technology catalog

- **US-17.1** — As a member, I want to add a technology to the catalog (name, category, icon), so that I can link it to my profile or to a project.
- **US-17.2** — As a member, I want to fix or delete a technology of the catalog, so that the catalog stays clean.

Acceptance criteria:

- the name of a technology is unique;
- the categories are: language, framework, database, tool and AI;
- deleting a technology in use asks for a confirmation that says how many profiles and projects will lose it.

### UC-18 — Manage a project

- **US-18.1** — As a member, I want to create a project as a draft (title, summary, presentation, dates, links, technologies), so that I prepare it before publishing it.
- **US-18.2** — As a project member, I want to publish or unpublish the project, so that I choose when it becomes visible.
- **US-18.3** — As a project member, I want to feature the project, so that it appears on the home page.
- **US-18.4** — As a project member, I want to delete the project, so that I remove an outdated project.
- **US-18.5** — As a project member, I want to preview the draft as visitors will see it, so that I can check it before publishing.

Acceptance criteria:

- the creator automatically becomes a member of the project;
- only the project members can edit it, publish it or see its draft;
- texts are entered in French and English;
- a deletion asks for confirmation;
- the preview uses the same page as the published project (`/projects/<slug>`), with a banner "Draft: only visible to the project members";
- a visitor, or a member who is not part of the project, gets a 404 page (see UC-05).

### UC-19 — Manage the members of a project

- **US-19.1** — As a project member, I want to add another member as a co-author, so that the project also appears on their portfolio.
- **US-19.2** — As a project member, I want to set the role of each member, so that visitors know who did what.

Acceptance criteria:

- a project always keeps at least one member: the database and the API refuse to remove its last member, with a translated error message;
- an account cannot be deleted while it is a member of a project: it must first be removed from its projects, and the projects where it is the only member must be deleted or get another member;
- the role is optional, but entered in both languages when set.

### UC-20 — Upload and manage media

- **US-20.1** — As a member, I want to upload an image for my avatar, or for the cover or gallery of a project, so that I illustrate my content.
- **US-20.2** — As a member, I want to enter the alternative text of each image, so that the website stays accessible.
- **US-20.3** — As a project member, I want to reorder or remove images of the gallery, so that I control how they are shown.

Acceptance criteria:

- accepted formats are JPEG, PNG and WebP for images (converted to WebP) and PDF for documents;
- the maximum size is 5 MB for an image and 10 MB for a PDF; a file that is too large is rejected with a translated message;
- EXIF data (including the GPS position) is removed and the file gets a random name;
- deleting an image used as an avatar or a cover simply removes it from where it was shown;
- deleting an account keeps the images it added to projects; its personal files that no project uses (avatar, CVs) are deleted with the account.

### UC-21 — Write and read recommendations

- **US-21.1** — As a member, I want to write a recommendation about another member, so that I highlight their work.
- **US-21.2** — As a visitor, I want to read the recommendations shown on a portfolio, so that I get another view of the member.
- **US-21.3** — As a member, I want to accept or hide a recommendation about me, so that I keep control of what is shown on my portfolio.

Acceptance criteria:

- a member cannot recommend themselves;
- recommendations from outside people are not planned (moderation, GDPR);
- a new recommendation is not visible until the recommended member accepts it;
- the recommended member can later hide an accepted recommendation;
- the author can edit or delete their recommendation; an edit puts it back to pending acceptance;
- a table must be added to the database schema, with a status (`pending`, `accepted`, `hidden`).

### UC-22 — Publish and read the devlog

- **US-22.1** — As a member, I want to publish an article about a solved problem or a technology I discovered, so that I share what I learn.
- **US-22.2** — As a visitor, I want to read the devlog articles, so that I see how the team thinks.

Acceptance criteria:

- an article is written in French and English, and can stay a draft like a project;
- the database schema is still to be designed.

---

## 9. Priorities

### 9.1 Version 1: required

- View the home page, the portfolios, the projects and the About page (UC-01 to UC-06)
- Switch the language and the light / dark mode (UC-07, US-07.1 and US-07.2)
- Log in and manage all one's content from the private area (UC-12 to UC-20)

### 9.2 Version 1.1: wanted

- Color themes (UC-07, US-07.3)
- Search, timeline and statistics (UC-08 to UC-10)
- Easter egg (UC-11)

### 9.3 Last

- Recommendations (UC-21)
- Devlog (UC-22)

---

## 10. Out of scope

These ideas were studied and then dropped, because they blur the professional message of the portfolio: badges and achievements, soundboard, coffee counter, mood of the day, quote of the month, availability calendar, "recruiter mode" to hide the non-professional content.
