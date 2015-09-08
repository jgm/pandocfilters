
# normal diff

This is a example for a in-file diff view

```bash
diff --git a/recipes-kernel/linux/files/hardware.cfg b/recipes-kernel/linux/files/hardware.cfg
index 9f61293..042a17c 100644
--- a/recipes-kernel/linux/files/hardware.cfg
+++ b/recipes-kernel/linux/files/hardware.cfg
@@ -1,5 +1,6 @@
 # rtc clock
 CONFIG_RTC_DRV_M41T80=y
+CONFIG_RTC_DRV_M41T80_WDT=n
 # cpu thermal support
 CONFIG_THERMAL=y
 CONFIG_CPU_THERMAL=y
```

# git filter extension

This diff is generated from `git-filter` extension.

```{.git-filter commit-range="1.1.1..1.2.4" objects="../README" diffoptions="-U0"}
HEADER
```

This is some text after the generated diff-part.
