### Pages

**Program Builder**
```
└── Program Builder
    ├── src.core.login --> enforce_login
    ├── src.core.state --> initialise_state
    ├── src.ui.screens.program_builder.state --> init_program_builder_state
    └── src.ui.screens.program_builder.nav --> render_program_builder_tabs
        └── Mobile
            └──
        └── Desktop
            ├── if desktop_program_builder_screen == 'dimensions_form' then src.ui.screens.program_builder.desktop_dimensions_form --> render_desktop_dimensions_form
            ├── if desktop_program_builder_screen == 'movement_selection' then src.ui.screens.program_builder.desktop_movement_selection --> render_desktop_movement_selection
            └── if desktop_program_builder_screen == 'progressions' then src.ui.screens.program_builder.desktop_progressions --> render_desktop_progressions
        └── Settings
            └──
```


### Screen Folder Structure

The application follows a "Feature Based" directory approach, starting with a folder for a top-level feature, followed by a file for each screen contained within that feature.
The feature level also includes a feature specific navigation and state file.
Features are currently aligned to 'Pages', so that each feature has its own subdomain, and page, within the application.

```
└── 📁screens
    └── 📁program_builder
        ├── nav.py
        ├── state.py
        ├── desktop_dimensions_form.py
        ├── desktop_movement_selection.py
        └── desktop_progressions.py
```


### State Management
To maintain a clean state and take advantage of Streamlit's attribute access syntax, all keys in st.session_state use an underscore-prefixed naming convention.

**Namespace Pattern:** [feature]_[variable_name]

Namespace | Responsibility | Example Key (Attribute Access)
--- | --- | ---
nav_ | Global UI position | st.session_state.nav_active_feature
auth_ | User session data | st.session_state.auth_user_id
program_builder_ | Program Builder data | st.program_builder_desktop_screen

The top level of state management, in ```core/state.py``` is responsible for:
1. Managing the states that may need to be accessed by either: multiple features, or by features in which they aren't created (cross-feature state checking).
2. Configuration settings like whether the sidebar is collapsed.
3. User information that may need to be accessed outside of the login function.
4. High-level features that track the global position of the user, in order to clear out or reset feature-specific states when the user navigates to another page.

Feature-specific states will be initialised on the feature page, ```page/page_name.py```, from the ```screens/feature/state.py``` file.

An example of of initialisation using Python's attrribute notation:

```
import streamlit as st

if 'active_feature' not in st.session_state:
    st.session_state.active_feature = None
```

And using a feature specific state:

```
from ui.screens.state import init_feature_state

init_feature_state()
```

Lastly, state functions can exist for specific screens within a feature, e.g. for a screen named desktop_dimensions_form, ```init_desktop_dimensions_form_state```, would be called at the top of ```desktop_dimensions_form.py```.

**First Run Protection**: Outside of the enforce login function, if a user bookmarks a subdomain, they may be met with a KeyError if a state variable is accessed that isn't initialised on the bookmarked page. Having a minimum global ```initialise_state()``` that can be called on every page will prevent these crashes.


### Navigation

The top level of navigation happens in each page, at ```pages/page_name.py``` by calling a central function which sets the session state for the active feature and calls a feature specific renderer.

```
import streamlit as st
from ui.navigation import state_and_render
from ui.screens.feature.nav import render_feature

state_and_render("feature_name", render_feature)
```

Whilst each page could call the rendering function for that feature directly, having a centralised function that hands off to the feature allows for additional logic to be applied whenever a user changes between pages.

The central function looks like this, handling ```st.session_state.current_feature == 'my_feature'```, this allows the global navigation to remain decoupled from features.

```
def state_and_render(feature_name, render_func):
    """
    Standardizes how physical pages hand off to feature folders.
    """
    # Sync state
    st.session_state.nav_active_feature = feature_name
    
    # Run any global logic
    
    # Execute the specific feature
    render_func()
```

An example of a feature specific navigation is ```ui.screens.program_builder.nav``` and importing ```render_feature_nav```.

The feature specific navigation would then use an if / else block to handle the rendering of specific screens inside the feature.

```
import streamlit as st
from ui.screens.feature.first_expected_screen import render_first_expected_screen

def render_feature():
    feature_screen = st.session_state.get('feature.active_screen')

    if feature_screen == 'first_expected_screen':
        render_first_expected_screen()
```

An example of a feature specific rendering function is ```ui.screens.program_builder.desktop_dimensions_form``` and importing ```render_desktop_dimensions_form```.

Additional navigation functions exist that, such as rendering tabs, which form an overall navigation hierarchy:

```
└── Global Navigation - Tracks Page / Feature
    └── Tab Navigation - For "in-page" navigation that is visible to the user
        ├── Screen Navigation - Different screens that make up a user journey inside of a tab
```