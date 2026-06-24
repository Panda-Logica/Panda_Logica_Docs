# Setting Up a Report in MBI

_Last updated: 2026-06-15_

This guide shows how to open a report, choose the right view, apply filters, and save your setup so you can reuse it next time.

> **Who is this for?** Everyday MBI users. If you need to **create a new report definition** for your organisation, ask your MBI administrator — that work is done in the MBI Designer tool, not covered here.

## Before you start

- MBI is installed and activated (see **[First Login](../getting-started/first-login.md)**).
- You are connected to your company environment.
- Your administrator has given you access to at least one report.

---

## 1) Open a report

1. Launch **MBI**.
2. In the **left menu**, expand the report category (for example *Sales*, *Stock*, or *Finance*).
3. Click the report you want to run.

MBI opens the report in a new tab. Most reports have two views:

| Tab | Use it for |
|-----|------------|
| **Dashboard** | Charts, KPIs, and summary visuals |
| **Grid** | Detailed rows you can filter, sort, group, and export |

![Sales Overview report open in MBI with the left menu and Grid tab visible](../screenshots/Screenshot%202026-03-25%20113208.jpg)

---

## 2) Set the date range (if prompted)

Many reports use a **From** and **To** date.

1. Open the **Date Selection** panel on the left menu.
2. Set the period you want to analyse.
3. Click the report name again to refresh the data.

> **Tip:** If results look empty, widen the date range first before changing anything else.

The left menu also includes **Initial Query Load Options** for controlling how much data is loaded when the report first runs.

![Left menu showing Date Selection and report categories](../screenshots/Screenshot%202026-03-25%20113151.jpg)

---

## 3) Choose a dashboard layout

If the report includes dashboards:

1. Open the **Dashboard** tab for the report.
2. Use the **dashboard list** on the left to pick a layout:
   - **Standard** — shared layouts provided by your administrator
   - **Personal** — layouts you have saved yourself
3. MBI remembers your last choice for that report.

---

## 4) Work with the grid

Switch to the **Grid** tab when you need line-level detail.

Common tasks:

- **Filter a column** — click the filter icon in the column header, or use **Edit Filter** at the bottom of the grid.
- **Sort** — click a column header.
- **Group rows** — drag a column header into the group panel above the grid.
- **Show or hide columns** — use the column chooser from the grid menu.
- **Export** — use the export option on the ribbon to send results to Excel or PDF.

### Apply filters

Active filters are shown in the bar at the bottom of the grid. Use **Edit Filter** to add or change criteria.

![Grid with filters applied — Customer name and Status](../screenshots/Screenshot%202026-03-25%20113208.jpg)

### Group and summarise data

Drag column headers such as **Invoice date** or **Arrears days** into the grouping area above the grid. MBI nests the data and can show subtotals for each group.

![Grid grouped by Invoice date and Arrears days](../screenshots/Screenshot%202026-03-25%20113300.jpg)

Right-click a grouped numeric column to choose a summary function — **Sum**, **Min**, **Max**, **Count**, or **Average**.

![Summary options on a grouped column](../screenshots/Screenshot%202026-03-25%20115219.jpg)

For more complex analysis, add several grouping levels — for example **Ship method code**, **Warehouse**, and **City** — and expand or collapse each level as needed.

![Multi-level grouping with subtotals](../screenshots/Screenshot%202026-03-25%20115235.jpg)

### Drill down to related data

Right-click a row or cell to open **related reports** (where your administrator has configured them). For example, from **Sales Overview** you can jump straight to **Shipments** for the selected customer.

![Right-click menu showing related reports](../screenshots/Screenshot%202026-03-25%20114602.jpg)

![Shipments report opened from Sales Overview](../screenshots/Screenshot%202026-03-25%20114634.jpg)

On the Shipments grid you can switch between saved layouts such as **By Customer and date** or **By WHS and Ship Method**, and group by fields like **Ship method code** and **Warehouse**.

![Shipments layout grouped by warehouse and ship method](../screenshots/Screenshot%202026-03-25%20114715.jpg)

![Grouping area with Ship method code and Warehouse](../screenshots/Screenshot%202026-03-25%20114941.jpg)

---

## 5) Save your layout

After you arrange columns, filters, grouping, or sorting the way you want:

1. On the ribbon, open the **Layouts** tab.
2. Click **Save Current Layout As** (for a new layout) or **Save Current Layout** (to update the one in use).
3. Enter a clear name (for example `Method, City and Qty` or `March Sales by Region`).
4. Click **Save**.

Your saved layouts appear in the **Layouts** gallery on the ribbon. Select one anytime to restore that view.

![Layouts tab with saved layout options](../screenshots/Screenshot%202026-03-25%20113151.jpg)

![Enter a name for a new layout](../screenshots/Screenshot%202026-03-25%20115300.jpg)

![Saving a new layout called Method, City and Qty](../screenshots/Screenshot%202026-03-25%20115335.jpg)

Once saved, your layout appears alongside the standard options and can be selected with one click.

![Newly saved layout selected in the Layouts gallery](../screenshots/Screenshot%202026-03-25%20115355.jpg)

---

## 6) Run the same report again later

Next time you open the report:

- MBI restores your last **dashboard** and **grid layout** automatically.
- Adjust the date range if needed, then refresh.

---

## Quick checklist

| Step | Done? |
|------|-------|
| Report opened from the left menu | ☐ |
| Date range set correctly | ☐ |
| Dashboard or Grid view selected | ☐ |
| Filters / grouping applied | ☐ |
| Layout saved with a meaningful name | ☐ |

---

## Troubleshooting

**I cannot see any reports in the menu.**  
Your user account may not have permission yet. Contact your MBI administrator.

**The report runs but shows no rows.**  
Check the date range, filters, and whether you have access to the underlying data area.

**I saved a layout but cannot find it.**  
Open the same report, go to the **Grid** tab, and check the **Layouts** gallery on the ribbon.

**I need a report that is not in the menu.**  
Ask your administrator to publish it. New report definitions are created in **MBI Designer**, then assigned to users or groups.

---

## Related guides

- **[First Login](../getting-started/first-login.md)** — activation and connecting to your data source
- **Support:** support@pandalogica.com
