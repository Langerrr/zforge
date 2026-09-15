# Session Log

> Tracks which sessions contributed to this feature, and how each one ended.

One row per session, written when the session ends. Nothing above the table: a milestone, a pause or an adjudication has its home in the phase file, and the table is the log.

**Models** names the pair the session ran on — `{implementation} / {acceptance}`. A resumed session proposes the previous row's pair.

**Ended** is one of: `completed` · `handed off` · `usage limit` · `error` · `abandoned`.
Usage-limit endings are a budgeting signal — several in one run means the schedule is asking for more concurrent tokens than the run has.

| Session ID | Date | Phases Touched | Models | Ended | Summary |
|------------|------|----------------|--------|-------|---------|
