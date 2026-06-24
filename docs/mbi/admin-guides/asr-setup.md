# ASR Setup

_Last updated: 2026-06-15_

This guide explains how to configure the **ASR (Admin System Repository)** — the metadata layer MBI uses before users can run reports. ASR stores your table definitions, field properties, master/slave relationships, and the foundation queries are built on.

> **Who is this for?** MBI administrators setting up a new environment or extending an existing one. End users do not need ASR access.

## ASR vs TSR

MBI separates **metadata** from **live data**:

| Layer | Name | What it holds |
|-------|------|----------------|
| **ASR** | Admin System Repository | Registered tables, fields, joins, calculated fields, query definitions |
| **TSR** | Target System Repository | Your operational database — IBM i, SQL Server, etc. |

ASR setup defines *what exists and how it connects*. TSR is where report data is read from at runtime. Configure the target connection first (see **[TSR Setup](tsr-setup.md)**), then complete ASR setup in this guide.

---

## Before you start

- You have **administrator** rights in MBI.
- An **environment** exists (or you can create one).
- The **target database** is reachable from the MBI workstation.
- You know which schemas/libraries and tables you want to expose (for example sales headers, shipment lines, item master).

---

## 1) Open System Admin

1. Launch **MBI** and connect to your environment.
2. On the ribbon, open **System admin** (or use the options menu equivalent).
3. **System Admin** opens — this is the MQ Setup application.

The main tabs you will use for ASR are:

| Tab | Purpose |
|-----|---------|
| **Environments** | Create environments, ASR database location, target platform, schemas |
| **Tables and Fields** | Import tables, define primary keys, master/slave links, calculated fields |
| **Queries** | Create and maintain query/report definitions (after ASR metadata exists) |

---

## 2) Create or configure an environment

If you are starting from scratch:

1. Go to **Environments**.
2. Click **Create new environment** and complete the wizard:
   - **Environment name** — how users will recognise this connection.
   - **ASR DB platform** — where metadata is stored (MS Access, SQL Server, or IBM i).
   - **ASR DB location / schema** — physical location of the ASR database.
   - **Target DB platform** — IBM i (**System i**) or **SQL Server** for live data.
   - **Target connection** — server, credentials, and catalog details.
3. Click **Accept changes** to save environment details.

For an existing environment, select it in the list and verify:

- **ASR DB location** and **ASR DB schema** are correct.
- **Target DB platform** matches your ERP/database.
- **Target IP** and connection settings are valid.

### Add schemas (ERP systems)

Each schema maps an ERP nickname to a library or catalog on the target system:

1. With the environment selected, click **Add new Schema(s)**.
2. Register the schema nickname and library name (for example `IBM_ERP` → `MYLIB`).
3. Save changes.

> You must define at least one schema before you can import tables.

---

## 3) Import tables and fields from the target system

ASR learns table structure from TSR — you do not type every column manually.

1. Open **Tables and Fields**.
2. On the **Define Master Tables and Primary keys** sub-tab, click **Add new table/file**.
3. In the file picker:
   - Select the **schema** (ERP nickname).
   - MBI lists tables/files available on the target system that are not already in ASR.
   - Select one or more tables (use **Select All** if needed).
   - Click **Add Selected** (or right-click → **Add File to database**).
4. Wait for the progress screen to finish — it reads field definitions from the target and writes them into ASR (`MFF` for tables, `MFFD` for fields).

When complete:

- The **All Files** grid lists registered tables.
- Click a table row to load its fields in the **Fields For table** panel on the right.

Repeat for every table your reports will need. Import related tables together (for example order header and order lines) so joins can be defined next.

---

## 4) Define primary keys and master/slave relationships

Master/slave links tell MBI how tables join — for example when a line table stores a product code that should resolve to the item master.

### Set the primary key on a master table

1. In **All Files**, click the master table (for example item master).
2. In the fields grid, **right-click** the primary key column.
3. Choose **Set/view Primary Key**.
4. When prompted, choose whether to search **all fields** or only fields with **similar attributes** to the key you selected.

MBI shows candidate **slave fields** in other tables that may refer to this master.

### Link slave fields to the master

1. From the **similar fields** list, **drag** matching slave fields into the **master/slave links** grid.
   - Example: drag `LPROD` from an order line table to link it to `IPROD` on the item master.
2. Click **Accept changes** to save the `MFMF` relationships.

MBI will:

- Record the master field on the table (`MFF`).
- Store slave → master mappings (`MFMF`).
- Update existing query field references where slave fields were already used.

> Each table can have **one primary key**. To change it, unset the existing key first.

---

## 5) Optional: calculated fields

Use calculated fields when users need derived values not stored on the source table.

1. Open the **Define Calculated Fields** sub-tab under **Tables and Fields**.
2. Choose **Schema** and **Table** the field belongs to.
3. Enter:
   - **Field name** and **Field text** (display label).
   - **Field expression** — use the field finder panels to pick columns from registered tables.
   - **Field type** (character or numeric) and **Pivot type** if used in dashboards.
4. Click **Add new calculated field** (or **Update calculated field** when editing).

See **[Calculated Fields](../advanced/calculated-fields.md)** for expression examples.

---

## 6) Optional: dropdown lookups (single-record forms)

For fields that should show a dropdown instead of a raw code:

1. Open **Define a Table's single record form**.
2. Select the table and field.
3. Click **Add/Edit Dropdown box lookup details for selected field**.
4. Configure:
   - **Lookup table schema** and **Lookup table**
   - **Value/key field** and **Display field**
   - Optional **Where clause** and **Category**
5. Save — the field's display type is set to **Combo**.

---

## 7) Verify your setup

Before assigning reports to users, confirm ASR is complete:

| Check | How to verify |
|-------|----------------|
| Tables imported | All required tables appear in **All Files** |
| Fields present | Click each table — field list matches expectations |
| Primary keys set | Master tables show a defined primary key |
| Joins linked | Slave codes resolve to master tables via **Accept changes** |
| Test query | Use **Queries → Wizard to create a Query** with the new tables |

Once a test query runs successfully in MBI, assign it to groups/roles and point users to **[Setting Up a Report](../user-guides/setting-up-a-report.md)**.

---

## Recommended setup order

```
Environment + target connection
        ↓
Add schema(s)
        ↓
Import tables/fields from target
        ↓
Define primary keys + master/slave links
        ↓
(Optional) Calculated fields + dropdown lookups
        ↓
Create queries and assign to users
```

---

## Troubleshooting

**Add new table/file shows no schemas.**  
Add a schema under **Environments → Add new Schema(s)** for the selected environment first.

**Field data is still loading.**  
Wait for the background load to finish, then click the table again.

**Cannot set a second primary key.**  
Each table allows one primary key. Clear or change the existing key before assigning another.

**Slave field links do not appear in queries.**  
Click **Accept changes** on the master/slave panel after dragging links. Existing queries may need their fields refreshed.

**Import fails or returns no tables.**  
Check TSR connectivity (server, library/catalog, credentials). See **[TSR Setup](tsr-setup.md)**.

**I lack menu options in System Admin.**  
Your user needs admin rights or specific permissions such as *Add a File* and *Define Master/Slave fields*. See **[Roles](roles.md)**.

---

## Related guides

- **[TSR Setup](tsr-setup.md)** — connect MBI to IBM i or SQL Server
- **[Roles](roles.md)** — users, groups, and report access
- **[Calculated Fields](../advanced/calculated-fields.md)** — expressions and pivot types
- **[Setting Up a Report](../user-guides/setting-up-a-report.md)** — end-user report workflow
- **Support:** support@pandalogica.com
