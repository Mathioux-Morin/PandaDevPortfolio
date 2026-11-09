CREATE TABLE users(
   idUser INT,
   password_changed_at DATETIME NOT NULL DEFAULT now(),
   login VARCHAR(50) NOT NULL,
   password_hash VARCHAR(255) NOT NULL,
   PRIMARY KEY(idUser),
   UNIQUE(login)
);

CREATE TABLE profiles(
   idUser INT,
   slug VARCHAR(255) NOT NULL,
   updated_at DATETIME NOT NULL,
   created_at DATETIME NOT NULL DEFAULT now(),
   display_name VARCHAR(50) NOT NULL,
   contact_email VARCHAR(255),
   contact_phone VARCHAR(16) CHECK (contact_phone ~ '^\+[1-9][0-9]{6,14}$'),
   availability VARCHAR(50) CHECK (enumerated),
   now L10n,
   now_updated_at DATETIME,
   headline L10n NOT NULL,
   bio L10n NOT NULL,
   location VARCHAR(50),
   is_public LOGICAL NOT NULL DEFAULT false,
   contact_form_enabled LOGICAL NOT NULL DEFAULT true,
   PRIMARY KEY(idUser),
   UNIQUE(slug),
   FOREIGN KEY(idUser) REFERENCES users(idUser)
);

CREATE TABLE experiences(
   idExperience INT,
   kind VARCHAR(50) NOT NULL CHECK (enumerated),
   organization VARCHAR(50) NOT NULL,
   description L10n NOT NULL,
   title L10n NOT NULL,
   location VARCHAR(50) Default NULL,
   start_on DATE NOT NULL,
   end_on DATE CHECK(end_on>=start_on),
   employment_status VARCHAR(50) CHECK(kind = 'work'),
   contract_type VARCHAR(50) CHECK (kind = 'work'),
   idUser INT NOT NULL,
   PRIMARY KEY(idExperience),
   FOREIGN KEY(idUser) REFERENCES users(idUser)
);

CREATE TABLE skills(
   idSkill INT,
   name L10n NOT NULL,
   category VARCHAR(50) NOT NULL CHECK (enumerated),
   icon VARCHAR(50),
   PRIMARY KEY(idSkill),
   UNIQUE(name)
);

CREATE TABLE media(
   idMedia UUID,
   storage_key VARCHAR(255),
   mime_type VARCHAR(50) CHECK (enumerated),
   width INT CHECK (width>0),
   height INT CHECK (height>0),
   size_bytes BIGINT NOT NULL CHECK (size_bytes>0),
   created_at DATETIME NOT NULL DEFAULT (now),
   alt L10n NOT NULL,
   idUser INT,
   PRIMARY KEY(idMedia),
   UNIQUE(storage_key),
   FOREIGN KEY(idUser) REFERENCES users(idUser)
);

CREATE TABLE link_kinds(
   kind VARCHAR(50),
   url_pattern VARCHAR(255),
   icon VARCHAR(50),
   PRIMARY KEY(kind)
);

CREATE TABLE social_links(
   idSocialLink INT,
   url VARCHAR(255) NOT NULL,
   position_ INT NOT NULL DEFAULT 0,
   label VARCHAR(50),
   idUser INT NOT NULL,
   kind VARCHAR(50) NOT NULL,
   PRIMARY KEY(idSocialLink),
   FOREIGN KEY(idUser) REFERENCES users(idUser),
   FOREIGN KEY(kind) REFERENCES link_kinds(kind)
);

CREATE TABLE projects(
   idProject INT,
   slug VARCHAR(255) NOT NULL,
   title L10n NOT NULL,
   summary L10n NOT NULL,
   demo_url VARCHAR(255),
   started_on DATE NOT NULL,
   ended_on DATE CHECK(on_ended>=started_on),
   is_published LOGICAL NOT NULL DEFAULT false,
   is_featured LOGICAL NOT NULL DEFAULT false,
   position_ INT NOT NULL DEFAULT 0,
   updated_at DATETIME NOT NULL DEFAULT now(),
   content L10n,
   repo_url VARCHAR(255),
   idMedia UUID,
   PRIMARY KEY(idProject),
   UNIQUE(idMedia),
   UNIQUE(slug),
   FOREIGN KEY(idMedia) REFERENCES media(idMedia)
);

CREATE TABLE experience_links(
   idExperienceLink INT,
   url VARCHAR(255) NOT NULL,
   position_ INT NOT NULL DEFAULT 0,
   label VARCHAR(50),
   idExperience INT NOT NULL,
   kind VARCHAR(50) NOT NULL,
   PRIMARY KEY(idExperienceLink),
   FOREIGN KEY(idExperience) REFERENCES experiences(idExperience),
   FOREIGN KEY(kind) REFERENCES link_kinds(kind)
);

CREATE TABLE masters(
   idUser INT,
   idSkill INT,
   score BYTE NOT NULL CHECK(score BETWEEN 0 AND 100),
   level VARCHAR(50) NOT NULL GENERATE ALWAYS AS (...) STORED,
   position_ INT NOT NULL DEFAULT 0,
   PRIMARY KEY(idUser, idSkill),
   FOREIGN KEY(idUser) REFERENCES users(idUser),
   FOREIGN KEY(idSkill) REFERENCES skills(idSkill)
);

CREATE TABLE works_on(
   idUser INT,
   idProject INT,
   role L10n,
   status VARCHAR(50) NOT NULL DEFAULT(pending),
   PRIMARY KEY(idUser, idProject),
   FOREIGN KEY(idUser) REFERENCES users(idUser),
   FOREIGN KEY(idProject) REFERENCES projects(idProject)
);

CREATE TABLE uses(
   idSkill INT,
   idProject INT,
   PRIMARY KEY(idSkill, idProject),
   FOREIGN KEY(idSkill) REFERENCES skills(idSkill),
   FOREIGN KEY(idProject) REFERENCES projects(idProject)
);

CREATE TABLE shows(
   idProject INT,
   idMedia UUID,
   position_ INT NOT NULL DEFAULT 0,
   PRIMARY KEY(idProject, idMedia),
   FOREIGN KEY(idProject) REFERENCES projects(idProject),
   FOREIGN KEY(idMedia) REFERENCES media(idMedia)
);

CREATE TABLE attaches(
   idUser INT,
   idMedia UUID,
   kind VARCHAR(50) NOT NULL,
   PRIMARY KEY(idUser, idMedia),
   FOREIGN KEY(idUser) REFERENCES profiles(idUser),
   FOREIGN KEY(idMedia) REFERENCES media(idMedia)
);

CREATE TABLE involves(
   idExperience INT,
   idSkill INT,
   PRIMARY KEY(idExperience, idSkill),
   FOREIGN KEY(idExperience) REFERENCES experiences(idExperience),
   FOREIGN KEY(idSkill) REFERENCES skills(idSkill)
);
