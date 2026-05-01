# SharePoint List Formatting — Visual Reference

CSS theme classes and Fluent UI icons. Load this when the request involves colors, icons, status indicators, severity styling, theme-aware backgrounds, font styling, or any visual decoration.

---

## CSS Classes

SharePoint provides built-in CSS classes that respect the site theme. Always prefer these over hardcoded colors.

### Severity / Status Classes (apply to parent div)
- `sp-field-severity--good` — green background (success/done)
- `sp-field-severity--low` — pale blue (in progress/info)
- `sp-field-severity--warning` — yellow/orange (warning/in review)
- `sp-field-severity--severeWarning` — darker orange (urgent/overdue)
- `sp-field-severity--blocked` — red background (blocked/critical)

### Theme Background Classes (ms-bgColor-*)
- `ms-bgColor-themePrimary`, `ms-bgColor-themeSecondary`, `ms-bgColor-themeTertiary`
- `ms-bgColor-themeDark`, `ms-bgColor-themeDarker`, `ms-bgColor-themeDarkAlt`
- `ms-bgColor-themeLight`, `ms-bgColor-themeLighter`, `ms-bgColor-themeLighterAlt`
- `ms-bgColor-neutralPrimary`, `ms-bgColor-neutralLight`, `ms-bgColor-neutralLighter`
- `ms-bgColor-white`, `ms-bgColor-black`
- `ms-bgColor-red`, `ms-bgColor-green`, `ms-bgColor-blue`, `ms-bgColor-orange`, `ms-bgColor-yellow`, `ms-bgColor-teal`, `ms-bgColor-purple`

### Contextual Background Classes (sp-css-backgroundColor-*)
- `sp-css-backgroundColor-BgPeach`, `sp-css-backgroundColor-BgGold`
- `sp-css-backgroundColor-BgLavender`, `sp-css-backgroundColor-BgMint`
- `sp-css-backgroundColor-successBackground50`, `sp-css-backgroundColor-warningBackground50`
- `sp-css-backgroundColor-errorBackground50`, `sp-css-backgroundColor-blockingBackground50`
- `sp-css-backgroundColor-blueBackground37`
- `sp-css-backgroundColor-noBackground` (transparent)

### Text Color Classes
- `ms-fontColor-themePrimary`, `ms-fontColor-themeSecondary`
- `ms-fontColor-neutralPrimary`, `ms-fontColor-neutralSecondary`, `ms-fontColor-neutralTertiary`
- `ms-fontColor-white`, `ms-fontColor-black`
- `ms-fontColor-red`, `ms-fontColor-green`, `ms-fontColor-blue`
- `sp-css-color-GreenFont`, `sp-css-color-YellowFont`, `sp-css-color-RedFont`, `sp-css-color-DarkRedFont`

### Font Size Classes
- `ms-fontSize-12`, `ms-fontSize-14`, `ms-fontSize-16`, `ms-fontSize-18`, `ms-fontSize-20`, `ms-fontSize-24`, `ms-fontSize-28`, `ms-fontSize-32`, `ms-fontSize-42`, `ms-fontSize-68`
- `sp-field-fontSize--small`, `sp-field-fontSize--standard`, `sp-field-fontSize--large`

### Font Weight Classes
- `ms-fontWeight-regular`, `ms-fontWeight-semibold`, `ms-fontWeight-bold`

### Border Classes
- `ms-borderColor-themePrimary`, `ms-borderColor-neutralLight`
- `sp-css-borderColor-neutralLight`, `sp-css-borderColor-neutralSecondary`
- `sp-field-borderAllRegular` — adds borders all around
- `sp-field-borderAllSolid` — solid border style

### Card and Row Layout Classes
- `sp-row-card` — standard card styling for rowFormatter
- `sp-row-title` — title text in card layout
- `sp-row-listPadding` — standard list padding
- `sp-row-button` — button styling in card layout
- `sp-card-container` — tile/card container
- `sp-card-defaultClickButton` — clickable card area
- `sp-card-subContainer` — inner card section

### Quick Action Classes
- `sp-field-quickActions` — styles an element as a quick action icon/button

---

## Fluent UI Icons

Use the `iconName` attribute to show any Fluent UI icon. Icons render as font glyphs and inherit text color.

### Commonly Used Icons by Category

**Status/Severity**: `CheckMark`, `Cancel`, `Warning`, `Error`, `ErrorBadge`, `Info`, `StatusCircleCheckmark`, `StatusCircleErrorX`, `Blocked`, `Completed`, `CompletedSolid`

**Navigation/Action**: `Forward`, `Back`, `ChevronRight`, `ChevronDown`, `ChevronUp`, `More`, `MoreVertical`, `Link`, `OpenInNewWindow`, `OpenInNewTab`

**Communication**: `Mail`, `Phone`, `Chat`, `Comment`, `Send`, `SkypeMessage`, `Video`

**People**: `Contact`, `ContactCard`, `People`, `Group`, `AddFriend`, `UserFollowed`

**Files/Documents**: `Document`, `Page`, `FileCode`, `PDF`, `ExcelDocument`, `WordDocument`, `PowerPointDocument`, `OneNoteLogo`, `Folder`, `FolderOpen`, `Attach`

**Calendar/Time**: `Calendar`, `Clock`, `DateTime`, `ScheduleEventAction`, `Event`

**Data/Charts**: `BarChartVertical`, `BarChart4`, `LineChart`, `PieDouble`, `AreaChart`, `DonutChart`

**Editing**: `Edit`, `EditNote`, `Delete`, `Add`, `Remove`, `Save`, `Undo`, `Redo`, `Copy`, `Paste`

**Trending**: `StockUp`, `StockDown`, `SortUp`, `SortDown`, `Trending12`, `Market`

**Misc Useful**: `FavoriteStar`, `FavoriteStarFill`, `Heart`, `HeartFill`, `Like`, `LikeSolid`, `Pin`, `Pinned`, `Flag`, `FlagFill`, `Emoji2`, `LocationDot`, `Home`, `Settings`, `Search`, `Filter`, `Refresh`

Full icon list: https://developer.microsoft.com/en-us/fluentui#/styles/web/icons
