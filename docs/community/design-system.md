# PyData Sphinx Theme Design System

The Pydata Sphinx Theme is committed to maintaining a theme that supports industry standards;
the design system must be included.
Whether choosing how to configure your theme or making changes to the design system itself,
consider the most recent version of the Web Content Accessibility Guidelines
(WCAG) to make sure the community continues to support documentation access for everyone.

## Guiding Principles

### Accessibility

Accessibility is at the core of the PyData Sphinx theme.
All design decisions are made with [WCAG 2.1](https://www.w3.org/TR/WCAG21/) conformance in mind,
ensuring that the theme is usable by people of all abilities.
Accessibility is a priority to make the theme inclusive for all users.

### Open Source Collaboration

As an open-source project, collaboration and transparency are key principles:

1. **Clear Guidelines:** All components, color palettes, and typography rules must be documented.
2. **Open Feedback:** Designers, developers, users and maintainers are encouraged
   to give feedback on the theme, helping to improve its functionality and usability over time.
   If you’d like to provide feedback, please open an issue on the
   [PyData Sphinx Theme GitHub repository.](https://github.com/pydata/pydata-sphinx-theme)
3. **Community Driven:** The theme grows and evolves based on the needs and
   suggestions of the open-source community.

## Typography

### Typeface

PyData Sphinx uses default system fonts.

### Type Scale

A type scale refers to the multiple by which font sizes increase.
You can find more about typographic scales at [Typographic Scale](https://designcode.io/typographic-scales).
For content-heavy websites, a medium contrast scale, which provides balanced
contrast between heading sizes without overly large jumps, is ideal,
typically ranging from `1.2x` to `1.33x`.

The PST type scale was updated (August 2024) to improve the accessibility of the
overall type system and increase visual contrast between the headings.
The PST type scale uses the Minor Third scale (`1.2x`) with values rounded to the
nearest even whole number.
Except for the H4 to H3 transition, all headings have a minimum of a `1.2x` increase,
which is an improvement over the previous scale.

### Styles

#### Headings

Headings create structure and hierarchy within the content.
They range from `H1` to `H6`, with each level decreasing in size and importance.

| Style     | Size (`px`) | Size (`rem`) | Weight | Use / Notes                      |
| :-------- | :---------- | :----------- | :----- | :------------------------------- |
| Heading 1 | 42          | 2.625        | 600    | Main page titles (use only once) |
| Heading 2 | 34          | 2.125        | 600    | Section titles                   |
| Heading 3 | 28          | 1.750        | 600    | Subsections within H2            |
| Heading 4 | 24          | 1.500        | 600    | Tertiary level headings          |
| Heading 5 | 20          | 1.250        | 600    | Less prominent headings          |
| Heading 6 | 16          | 1.000        | 600    | Lowest level headings            |

Always use headings in logical order (`H1`, `H2`, `H3`, etc.) without skipping levels,
to help assistive tech such as screen readers interpret the structure of the page.
Each page should have a single, unique `H1` to effectively define the page's purpose,
improving search engine optimization (SEO) and accessibility for users who rely
on assistive tech such as screen readers.

#### Body

Body text serves as the standard style for detailed content.
It is primarily used for longer, detailed content such as paragraphs, articles,
and descriptions, but may also apply to other areas such as modals, admonitions
or sections where longer content needs to be displayed clearly.

| Style | Size (`px`) | Size (`rem`) | Weight | Use / Notes                        |
| :---- | :---------- | :----------- | :----- | :--------------------------------- |
| Body  | 16          | 1.000        | 400    | Standard text size for readability |

While there is no absolute minimum text size, for optimum readability,
body text should be at least `16px`.

#### Links

Links must be styled in a way that makes them visually distinct from regular text.
All links should be underlined in addition to being color-coded,
as [color alone should not be used to convey meaning](https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html).

| Style | Size (`px`) | Size (`rem`) | Weight | Use / Notes                       |
| :---- | :---------- | :----------- | :----- | :-------------------------------- |
| Links | 16          | 1.000        | 400    | Always underlined and color-coded |

Links also have a hover and focus interactive state.
Hover and focus states should always show a change in color and visual design
to provide clear feedback for interactive elements.

Links are used to navigate between different pages or sections and to redirect
readers to external sources.
They are visually distinct from buttons, which are used to perform actions within
the current page or context and should not trigger actions like submitting forms
or toggling components.

#### Code Text

Code text is used to display inline code snippets or larger blocks of code.
It uses a monospaced font. The theme also includes interactive states for code
text including links.

### Type Color

Text color plays a crucial role in ensuring that content is legible and accessible.
In the PyData Sphinx theme, we use a predefined set of colors to ensure readability,
visual hierarchy, and consistency across different elements.
Each text color is designed to meet accessibility guidelines, ensuring sufficient
contrast between text and background.

When using colors in text, ensure that it meets the minimum
[WCAG color contrast accessibility criterion](https://www.w3.org/WAI/WCAG22/quickref/?versions=2.1#contrast-minimum).
Color alone should not be used to indicate meaning.
For example, text that is a link should not be indicated solely by color
but also with an underline.
This helps ensure that users who have difficulty distinguishing colors can still identify links.
Semantic colors (such as for success, warning, or error messages) can be used to
convey meaning, but color should not be the only indicator.
Pair these colors with icons or text labels to ensure clarity.

## Color

The PyData Sphinx theme uses a well-defined color palette to ensure consistency,
readability, and accessibility across the entire design system.
This color palette is available for both light and dark themes.
This document explains how to use the theme's color system

### Base Colors

Base colors form the foundation of the theme and are used across primary UI elements
like buttons, backgrounds, and text. They maintain consistency throughout the interface.

- **Primary**: The main color for major actions and interactive elements.
- **Secondary**: A supporting color for secondary actions and highlights.
- **Accent**: An emphasis color used sparingly for highlighting content.
- **Gray (Neutral)**: Used for typography, borders, and backgrounds.
- **Foundation Colors**: Black and white base colors used for backgrounds and
  surfaces (for example, cards, containers, modals) in light and dark modes.

Color variables are also documented in the [](../user_guide/styling.rst) section
of the User Guide.

### Semantic Colors

Semantic colors, colors named for what they represent and how they are used,
are provided for success, errors, warnings, and information.
Using these colors as named ensures users can easily understand system feedback
through visual cues.

## Relevant Links

For further reference, you can access the following resources related to the
color and typography in the PyData Sphinx theme:

1. **GitHub Repository:** The source code for the PyData Sphinx theme is available on GitHub.
   1. You can find the specific file that defines the typography settings,
      including font stacks, sizes, and weights in the
      [`fonts.scss` file](https://github.com/pydata/pydata-sphinx-theme/blob/main/src/pydata_sphinx_theme/assets/styles/variables/_fonts.scss).
   2. You can find all the PyData Sphinx theme colors in the
      [`color.scss` file](https://github.com/pydata/pydata-sphinx-theme/tree/main/src/pydata_sphinx_theme/assets/styles/variables/_color.scss)
2. **Figma Design File:** The Figma file contains the visual design and specifications
   for the typography styles, including font sizes, line heights,
   and spacing used throughout the theme. It also includes our color palette and its use cases, as well as details on interactive components and their states.
   You can access it [through this link to the Figma file][figma-library].

### References

1. [https://carbondesignsystem.com/elements/typography/overview/](https://carbondesignsystem.com/elements/typography/overview/)
2. [https://canvas.workday.com/styles/tokens/type](https://canvas.workday.com/styles/tokens/type)
3. [https://atlassian.design/foundations/typography-beta](https://atlassian.design/foundations/typography-beta)
   refer to the [Figma Design File](https://www.figma.com/community/file/1443191723065200671/pydata-sphinx-theme-design-system).

<!-- reusable links -->

[figma-library]: https://www.figma.com/community/file/1443191723065200671/pydata-sphinx-theme-design-system
