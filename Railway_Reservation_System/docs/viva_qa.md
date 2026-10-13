# COMPREHENSIVE DBMS VIVA QUESTION BANK & ANSWERS
## Railway Ticket Reservation and Journey Management System
**Academic Course:** Database Management Systems (B.Tech Computer Science & Engineering)

---

### Core Conceptual Questions & Answers

#### Q1: What is a Relational Database Management System (RDBMS)?
**Ans:** An RDBMS is a software system based on Edgar F. Codd's relational model where data is stored in structured tables (relations) consisting of rows (tuples) and columns (attributes). It enforces data integrity through schema definitions, domain constraints, keys, referential integrity, and ACID transaction guarantees.

#### Q2: Why was MySQL selected as the primary target database?
**Ans:** MySQL 8.x provides the robust **InnoDB transactional storage engine**, which guarantees full ACID compliance, supports row-level locking (`SELECT ... FOR UPDATE`), enforces foreign key referential integrity with cascading rules, handles multi-table views, supports standard SQL-92/SQL:1999 window functions, and efficiently processes concurrent reservations without table-level blocking.

#### Q3: What is an Entity-Relationship (ER) Diagram?
**Ans:** An ER diagram is a conceptual data modeling blueprint that graphically visualizes real-world entities (e.g., Train, Station, Passenger), their descriptive attributes, primary/candidate keys, and the cardinalities (1:1, 1:N, M:N) and participation constraints of relationships connecting them.

#### Q4: What is a Primary Key?
**Ans:** A primary key is a minimal candidate key chosen to uniquely identify each tuple in a relation. It enforces entity integrity: no attribute in the primary key may contain NULL values, and all values across rows must be distinct.

#### Q5: What is a Foreign Key?
**Ans:** A foreign key is an attribute or set of attributes in a relation that references the primary key of another (or the same) relation. It enforces referential integrity, ensuring that relationships between tables remain consistent and invalid orphan records cannot exist.

#### Q6: What are Functional Dependencies (FDs)?
**Ans:** A functional dependency $X \rightarrow Y$ between two sets of attributes $X$ and $Y$ in relation $R$ specifies that the value of $X$ uniquely determines the value of $Y$. If two tuples agree on attribute values of $X$, they must agree on attribute values of $Y$. FDs form the theoretical foundation for database normalization.

#### Q7: Explain 1NF, 2NF, and 3NF.
**Ans:**
- **1NF (First Normal Form):** All attribute values are atomic (indivisible scalars); no repeating groups or multivalued columns exist.
- **2NF (Second Normal Form):** Relation is in 1NF and contains no partial dependencies—every non-prime attribute is fully functionally dependent on the entire candidate key.
- **3NF (Third Normal Form):** Relation is in 2NF and contains no transitive dependencies—no non-prime attribute depends on another non-prime attribute (for every non-trivial $X \rightarrow Y$, $X$ is a superkey or $Y$ is a prime attribute).

#### Q8: Why are train runs different from train definitions in your schema?
**Ans:** A `train` represents static master catalog metadata (e.g., Train #22436, Vande Bharat Express, Route RT-NDLS-BSB). A `train_run` represents a specific dated operational run (e.g., Train #22436 operating on 14 October 2026). Decoupling them is mandatory for 3NF; otherwise, repeating train names for every calendar date causes update and insertion anomalies.

#### Q9: Why is a journey segment modeled as a separate entity?
**Ans:** In passenger rail operations, a train travels through ordered station sequences. Multiple passengers can occupy the same physical seat on non-overlapping intervals (e.g., Passenger A from Stop 1 to 2; Passenger B from Stop 2 to 4). `journey_segments` stores individual seat interval allocations $[start\_stop\_seq, end\_stop\_seq)$, enabling segment-wise seat reuse.

#### Q10: How does segment-wise seat allocation work?
**Ans:** Station stops are indexed with strictly increasing integers ($1, 2, 3 \dots$). A passenger's journey from origin to destination forms a half-open interval $[origin\_seq, dest\_seq)$. An existing allocation $[s, e)$ and a requested interval $[r_{start}, r_{end})$ overlap if and only if:
$$s < r_{end} \quad \text{AND} \quad r_{start} < e$$
If this condition evaluates to False for all active segments of a seat, the seat is available.

#### Q11: Why does a simple availability check query followed by an insert create a race condition?
**Ans:** If two concurrent transactions $T_1$ and $T_2$ both execute `SELECT seat WHERE ...` simultaneously, both observe the seat as free before either commits. Both then execute `INSERT`, resulting in a catastrophic double-booking of the same physical seat.

#### Q12: How are transactions and row locks used to resolve concurrency?
**Ans:** We wrap availability checking and allocation in an atomic database transaction. Using `SELECT ... FOR UPDATE`, an exclusive row lock is placed on the parent `TrainRun` or candidate `Seat`. Any competing concurrent transaction attempting to read or book that train run must wait until the first transaction commits or rolls back, serializing allocations safely.

#### Q13: What is referential integrity?
**Ans:** Referential integrity ensures that any foreign key value in a referencing table must match an existing primary key value in the referenced table, or be NULL. In MySQL, it is enforced via `FOREIGN KEY ... REFERENCES ... ON DELETE RESTRICT / CASCADE`.

#### Q14: What are indexes and what are their trade-offs?
**Ans:** Indexes are auxiliary B-Tree data structures that allow the database engine to find tuples matching query conditions in $O(\log N)$ time rather than performing full table scans $O(N)$. The trade-off is increased storage overhead and slower write performance during `INSERT`, `UPDATE`, and `DELETE` operations because the index must be rebalanced.

#### Q15: Why use DECIMAL instead of FLOAT or DOUBLE for monetary values?
**Ans:** Binary floating-point types (`FLOAT`, `DOUBLE`) use IEEE 754 base-2 representations, leading to precision loss and rounding errors (e.g., $0.1 + 0.2 = 0.30000000000000004$). `DECIMAL(10, 2)` stores exact fixed-point decimal values, eliminating rounding discrepancy in fares, payments, and refunds.

#### Q16: How are waitlist queue positions maintained?
**Ans:** Waitlist positions are scoped by $(run\_id, travel\_class)$ and assigned monotonically ($1, 2, 3 \dots$) using `MAX(position) + 1` inside an exclusive transaction lock. This guarantees strict FIFO ordering and uniqueness.

#### Q17: How does cancellation affect seat availability?
**Ans:** Cancelling a booking updates the associated `journey_segments.allocation_status` from `ACTIVE` to `CANCELLED`. Because availability queries filter exclusively on `allocation_status = 'ACTIVE'`, the segment immediately becomes available for future bookings or waitlist promotion.

#### Q18: How is refund consistency enforced?
**Ans:** Refunds are calculated deterministically (e.g., 20% cancellation deduction for confirmed tickets; flat ₹30 clerkage for waitlists). A dedicated `cancellations` table stores the audit record, and a unique constraint on `cancellations.booking_id` prevents duplicate cancellations or double refunds.

#### Q19: What is the difference between an INNER JOIN and an OUTER JOIN?
**Ans:** An `INNER JOIN` returns only rows that have matching keys in both tables. A `LEFT OUTER JOIN` returns all rows from the left table, along with matching rows from the right table; if no match exists, NULL values are returned for right-table columns (e.g., listing coaches with 0 bookings).

#### Q20: How are GROUP BY, HAVING, and aggregate functions used?
**Ans:** `GROUP BY` partitions rows into summary buckets based on distinct column values. Aggregate functions (`COUNT`, `SUM`, `AVG`) compute summary statistics per group. `HAVING` filters groups after aggregation (unlike `WHERE`, which filters individual rows before grouping).

#### Q21: How does the web frontend communicate with the database?
**Ans:** The browser communicates via HTTP GET/POST requests to Flask route handlers. Flask invokes backend service layers, which interact with the database using SQLAlchemy ORM or raw SQL execution over persistent connection pools.

---

### 5 Challenging Deep-Dive Viva Questions

#### 1. "Can ordinary MySQL CHECK constraints enforce the segment interval exclusion across multiple rows?"
**Ans:** No. Standard SQL `CHECK` constraints are row-level constraints evaluated strictly on the values of the individual row being inserted or updated. They cannot perform arbitrary cross-row subqueries or evaluate other rows in the table. Cross-row interval exclusion must be enforced via transactional row locking in the application service layer, or through database triggers with table locking, or PostgreSQL `EXCLUDE USING gist` range constraints.

#### 2. "What happens if a passenger cancelling on NDLS-BSB frees a seat, but the top waitlisted candidate is only traveling CNB-BSB?"
**Ans:** Our promotion algorithm re-verifies segment availability for the candidate's exact requested interval $[origin, dest)$. Since the candidate's journey $[2, 4)$ is a subset of the freed interval $[1, 4)$, the candidate is eligible and promoted! The remaining sub-segment $[1, 2)$ stays available in the pool for other travelers.

#### 3. "If a database transaction fails midway during payment insertion after inserting a booking, how is atomicity preserved?"
**Ans:** In ACID transactions, atomicity ensures "all or nothing" execution. If payment insertion fails or an exception is thrown, Flask invokes `db.session.rollback()`. InnoDB uses its undo logs (`undo_log`) to revert the uncommitted booking and segment insertions, restoring the database to its exact prior consistent state.

#### 4. "Why is Boyce-Codd Normal Form (BCNF) not strictly required for train_stops?"
**Ans:** In `train_stops`, we have overlapping candidate keys: $\{route\_id, stop\_sequence\}$ and $\{route\_id, station\_id\}$. While in 3NF every non-trivial dependency $X \rightarrow Y$ has $X$ as a superkey or $Y$ as a prime attribute, achieving strict BCNF in tables with overlapping composite candidate keys can sacrifice functional dependency preservation. 3NF strikes the optimal balance between redundancy elimination and dependency preservation.

#### 5. "How would the system scale to handle thousands of concurrent reservation requests during Tatkal booking hours?"
**Ans:** 
1. **Partitioning:** Partition `journey_segments` and `bookings` by `run_date` or `train_id`.
2. **In-Memory Inventory Cache:** Use Redis with atomic Lua scripts or bitmap intervals for preliminary seat locking before hitting the RDBMS.
3. **Optimistic Locking with Versioning:** For high read concurrency, use version columns to detect concurrent updates without long-held pessimistic locks.
4. **Database Read Replicas:** Route read-heavy searches (`train_stops`, `trains`, `fare_rules`) to read replicas, directing only write transactions to the primary database.
