'''
UI Design Specification for Chess Game
Professional layout with consistent margins, paddings, and spacing
'''

class UIConfig:
    '''Centralized UI configuration for consistent design'''

    # Window dimensions
    BOARD_SIZE = 480
    DASHBOARD_WIDTH = 320
    TOTAL_WIDTH = BOARD_SIZE + DASHBOARD_WIDTH  # 800px
    TOTAL_HEIGHT = BOARD_SIZE  # 480px

    # Board layout
    DIMENSION = 8
    SQUARE_SIZE = BOARD_SIZE // DIMENSION  # 60px

    # Colors - Board
    BOARD_LIGHT = (241, 218, 179)
    BOARD_DARK = (182, 136, 96)
    BOARD_SELECTED_LIGHT = (0, 188, 212)
    BOARD_SELECTED_DARK = (8, 168, 198)
    HIGHLIGHT_MOVE = (0, 188, 212, 50)
    HIGHLIGHT_CAPTURE = (173, 238, 126, 150)

    # Colors - Dashboard
    DASHBOARD_BG = (40, 40, 40)
    PANEL_BG = (50, 50, 50)
    TEXT_PRIMARY = (255, 255, 255)
    TEXT_SECONDARY = (200, 200, 200)
    TEXT_DISABLED = (120, 120, 120)

    # Colors - Evaluation Bar
    EVAL_WHITE = (220, 220, 220)
    EVAL_BLACK = (60, 60, 60)
    EVAL_BORDER = (100, 100, 100)

    # Colors - Menu
    BUTTON_BG = (70, 130, 180)
    BUTTON_HOVER = (100, 160, 210)
    BUTTON_ACTIVE = (50, 110, 160)
    BUTTON_BORDER = (255, 255, 255)

    # Colors - Game Over
    OVERLAY_BG = (0, 0, 0, 180)
    CHECKMATE_WHITE = (255, 255, 255)
    CHECKMATE_BLACK = (50, 50, 50)
    DRAW_COLOR = (200, 200, 0)

    # Colors - Check indicator
    CHECK_COLOR = (255, 0, 0)
    CHECK_BG = (255, 255, 0)

    # Spacing - Dashboard
    DASHBOARD_MARGIN = 10  # Outer margin from edge
    DASHBOARD_PADDING = 10  # Inner padding for panels
    SECTION_SPACING = 20  # Space between major sections
    LINE_SPACING = 5  # Space between lines of text

    # Spacing - Elements
    ELEMENT_MARGIN = 10  # Margin around UI elements
    BUTTON_PADDING_H = 20  # Horizontal padding in buttons
    BUTTON_PADDING_V = 12  # Vertical padding in buttons
    PANEL_PADDING = 15  # Padding inside panels

    # Sizes - Evaluation Bar
    EVAL_BAR_HEIGHT = 30
    EVAL_BAR_MARGIN = 10

    # Sizes - Buttons
    BUTTON_HEIGHT = 50
    BUTTON_WIDTH = 250
    BUTTON_BORDER_RADIUS = 10
    BUTTON_BORDER_WIDTH = 2

    # Sizes - Panels
    PANEL_BORDER_RADIUS = 5
    PANEL_BORDER_WIDTH = 1

    # Fonts
    FONT_LARGE = 36  # Main titles, game over
    FONT_MEDIUM = 24  # Section headers, buttons
    FONT_SMALL = 18  # Regular text, move history
    FONT_TINY = 14  # Captions, timestamps

    # Animation
    FPS = 30
    ANIMATION_DURATION = 0.3  # seconds

    # Menu Layout
    MENU_TITLE_Y = 80
    MENU_BUTTONS_START_Y = 150
    MENU_BUTTON_SPACING = 70

    # Dashboard Layout Specification
    @staticmethod
    def get_dashboard_layout():
        '''Returns calculated positions for dashboard elements'''
        x = UIConfig.BOARD_SIZE
        margin = UIConfig.DASHBOARD_MARGIN
        width = UIConfig.DASHBOARD_WIDTH - (2 * margin)

        layout = {
            'x_base': x + margin,
            'width': width,
            'sections': []
        }

        y = margin

        # Game Mode Section
        layout['sections'].append({
            'name': 'game_mode',
            'y': y,
            'height': UIConfig.FONT_MEDIUM + UIConfig.LINE_SPACING,
            'font_size': UIConfig.FONT_MEDIUM
        })
        y += UIConfig.FONT_MEDIUM + UIConfig.SECTION_SPACING

        # Turn Indicator Section
        layout['sections'].append({
            'name': 'turn',
            'y': y,
            'height': UIConfig.FONT_MEDIUM + UIConfig.LINE_SPACING,
            'font_size': UIConfig.FONT_MEDIUM
        })
        y += UIConfig.FONT_MEDIUM + UIConfig.SECTION_SPACING

        # Opening Name Section
        layout['sections'].append({
            'name': 'opening',
            'y': y,
            'height': UIConfig.FONT_SMALL + UIConfig.LINE_SPACING,
            'font_size': UIConfig.FONT_SMALL
        })
        y += UIConfig.FONT_SMALL + UIConfig.SECTION_SPACING

        # Evaluation Bar Section
        layout['sections'].append({
            'name': 'eval_bar',
            'y': y,
            'height': UIConfig.EVAL_BAR_HEIGHT + (2 * UIConfig.EVAL_BAR_MARGIN),
            'bar_height': UIConfig.EVAL_BAR_HEIGHT,
            'margin': UIConfig.EVAL_BAR_MARGIN
        })
        y += UIConfig.EVAL_BAR_HEIGHT + (2 * UIConfig.EVAL_BAR_MARGIN) + UIConfig.SECTION_SPACING

        # Captured Pieces Section
        layout['sections'].append({
            'name': 'captured',
            'y': y,
            'height': UIConfig.FONT_TINY + (3 * UIConfig.LINE_SPACING) + 40,
            'title_font': UIConfig.FONT_TINY,
            'text_font': UIConfig.FONT_TINY
        })
        y += UIConfig.FONT_TINY + (3 * UIConfig.LINE_SPACING) + 40 + UIConfig.SECTION_SPACING

        # Move History Section (fills remaining space)
        layout['sections'].append({
            'name': 'move_history',
            'y': y,
            'height': UIConfig.TOTAL_HEIGHT - y - margin,
            'title_font': UIConfig.FONT_TINY,
            'move_font': UIConfig.FONT_TINY,
            'line_height': UIConfig.FONT_TINY + UIConfig.LINE_SPACING
        })

        return layout

    @staticmethod
    def get_menu_layout():
        '''Returns calculated positions for menu elements'''
        layout = {
            'title': {
                'y': UIConfig.MENU_TITLE_Y,
                'font_size': UIConfig.FONT_LARGE
            },
            'buttons': []
        }

        y = UIConfig.MENU_BUTTONS_START_Y
        button_count = 4

        for i in range(button_count):
            layout['buttons'].append({
                'x': (UIConfig.TOTAL_WIDTH - UIConfig.BUTTON_WIDTH) // 2,
                'y': y,
                'width': UIConfig.BUTTON_WIDTH,
                'height': UIConfig.BUTTON_HEIGHT,
                'font_size': UIConfig.FONT_MEDIUM
            })
            y += UIConfig.BUTTON_HEIGHT + UIConfig.MENU_BUTTON_SPACING

        return layout

    @staticmethod
    def get_promotion_dialog_layout():
        '''Returns layout for pawn promotion dialog'''
        dialog_width = 260
        dialog_height = 120

        return {
            'x': (UIConfig.BOARD_SIZE - dialog_width) // 2,
            'y': (UIConfig.TOTAL_HEIGHT - dialog_height) // 2,
            'width': dialog_width,
            'height': dialog_height,
            'padding': 15,
            'piece_size': 50,
            'piece_spacing': 10,
            'title_font': UIConfig.FONT_MEDIUM,
            'border_radius': 10,
            'border_width': 3
        }

    @staticmethod
    def get_game_over_layout():
        '''Returns layout for game over overlay'''
        return {
            'overlay_alpha': 180,
            'message_y': UIConfig.TOTAL_HEIGHT // 2 - 20,
            'instruction_y': UIConfig.TOTAL_HEIGHT // 2 + 20,
            'message_font': UIConfig.FONT_LARGE,
            'instruction_font': UIConfig.FONT_MEDIUM
        }

    @staticmethod
    def get_check_indicator_layout():
        '''Returns layout for check indicator'''
        return {
            'x': UIConfig.BOARD_SIZE // 2 - 80,
            'y': 10,
            'font_size': UIConfig.FONT_LARGE,
            'padding_h': 20,
            'padding_v': 10,
            'border_radius': 5
        }


# Design Guidelines
DESIGN_GUIDELINES = '''
Chess Game UI Design Guidelines
================================

1. SPACING HIERARCHY
   - Primary sections: 20px spacing
   - Secondary elements: 10px spacing
   - Text lines: 5px spacing
   - Margins: 10px from edges

2. COLOR USAGE
   - Dark dashboard (40,40,40) for reduced eye strain
   - High contrast text (255,255,255) for readability
   - Consistent highlight colors for interactivity
   - Muted colors for secondary information

3. TYPOGRAPHY
   - Large (36px): Titles, important messages
   - Medium (24px): Section headers, buttons
   - Small (18px): Regular content
   - Tiny (14px): Captions, metadata

4. INTERACTIVE ELEMENTS
   - Buttons: Clear hover states with color change
   - Borders: 2px for emphasis, 1px for subtle separation
   - Radius: 10px for buttons, 5px for panels
   - Padding: Minimum 10px for clickable areas

5. LAYOUT PRINCIPLES
   - Left: 480px board (fixed, square)
   - Right: 320px dashboard (vertical scroll if needed)
   - Responsive to content but fixed width
   - Clear visual hierarchy with spacing

6. ACCESSIBILITY
   - Sufficient color contrast (4.5:1 minimum)
   - Clear focus indicators for keyboard navigation
   - Text size minimum 14px for readability
   - Non-color coding (shapes + colors for states)

7. CONSISTENCY
   - All margins follow base-10 system (10, 20, 30...)
   - Font sizes follow 6px increments (14, 18, 24, 36)
   - Colors defined once in UIConfig
   - Spacing defined in UIConfig for reuse
'''
