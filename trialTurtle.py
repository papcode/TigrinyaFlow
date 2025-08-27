"""
Streamlit App for Ethiopian Amharic Characters with Hand-Drawing Animation
=========================================================================

This Streamlit application displays Ethiopian Amharic characters using animated SVG graphics
that simulate hand-drawing with stroke-by-stroke animation.
"""

import streamlit as st
import math
import time
from io import StringIO

# ==============================
# Global Parameters
# ==============================
LEFT_X = -30
RIGHT_X = 30
VERTICAL_HEIGHT = 100
CURVE_RADIUS = 20
SMALL_LINE_LENGTH = 20
CIRCLE_RADIUS = 15
EXTENSION_LENGTH = 35
TOP_GAP = 30
EXTRA_HEIGHT = 25
SVG_WIDTH = 300
SVG_HEIGHT = 350
STROKE_WIDTH = 4

class AnimatedSVGDrawer:
    """Class to handle animated SVG drawing operations with hand-drawing effect."""
    
    def __init__(self):
        self.strokes = []  # List of stroke dictionaries
        self.current_x = 0
        self.current_y = 0
        self.pen_down = True
        self.current_path = []
        self.stroke_delay = 0.5  # Delay between strokes in seconds
        
    def clear(self):
        """Clear all strokes."""
        self.strokes = []
        self.current_path = []
        
    def penup(self):
        """Lift the pen up."""
        if self.current_path and self.pen_down:
            self._add_stroke()
        self.pen_down = False
        
    def pendown(self):
        """Put the pen down."""
        self.pen_down = True
        self.current_path = [f"M {self.current_x} {self.current_y}"]
        
    def goto(self, x, y):
        """Move to a specific position."""
        if self.pen_down and self.current_path:
            self.current_path.append(f"L {x} {-y}")
        self.current_x = x
        self.current_y = -y
        if self.pen_down and not self.current_path:
            self.current_path = [f"M {x} {-y}"]
            
    def forward(self, distance, heading_degrees):
        """Move forward by distance in the given heading direction."""
        heading_radians = math.radians(heading_degrees)
        new_x = self.current_x + distance * math.cos(heading_radians)
        new_y = self.current_y - distance * math.sin(heading_radians)
        self.goto(new_x, -new_y)
        
    def circle(self, radius, extent=360):
        """Draw a circle or arc."""
        if not self.pen_down:
            return
            
        if self.current_path:
            self._add_stroke()
            
        # For circles, we'll create a special stroke type
        center_x = self.current_x + radius
        center_y = self.current_y
        
        if extent == 360:
            # Full circle
            stroke = {
                'type': 'circle',
                'cx': center_x,
                'cy': center_y,
                'r': abs(radius),
                'duration': 2.0  # Longer duration for circles
            }
            self.strokes.append(stroke)
        else:
            # Arc - use path
            end_angle = math.radians(extent)
            end_x = center_x + radius * math.cos(end_angle)
            end_y = center_y + radius * math.sin(end_angle)
            
            large_arc = 1 if abs(extent) > 180 else 0
            sweep = 1 if extent > 0 else 0
            
            path_data = (f"M {self.current_x} {self.current_y} "
                        f"A {abs(radius)} {abs(radius)} 0 {large_arc} {sweep} {end_x} {end_y}")
            
            stroke = {
                'type': 'path',
                'data': path_data,
                'duration': 1.5
            }
            self.strokes.append(stroke)
            self.goto(end_x, -end_y)
    
    def _add_stroke(self):
        """Add the current path as a stroke."""
        if self.current_path:
            path_data = " ".join(self.current_path)
            # Calculate stroke length for duration (longer strokes take more time)
            estimated_length = len(self.current_path) * 20  # Rough estimate
            duration = max(0.8, min(2.5, estimated_length / 100))
            
            stroke = {
                'type': 'path',
                'data': path_data,
                'duration': duration
            }
            self.strokes.append(stroke)
            self.current_path = []
    
    def get_animated_svg(self, title="Amharic Character", total_duration=None):
        """Generate animated SVG with hand-drawing effect."""
        if self.current_path and self.pen_down:
            self._add_stroke()
        
        if not total_duration:
            total_duration = len(self.strokes) * self.stroke_delay + sum(
                stroke.get('duration', 1.0) for stroke in self.strokes
            )
        
        # Transform coordinates to fit SVG viewport
        viewbox_x = LEFT_X - 50
        viewbox_y = -VERTICAL_HEIGHT - 80
        viewbox_width = (RIGHT_X - LEFT_X) + 100
        viewbox_height = VERTICAL_HEIGHT + 120
        
        # Generate animated strokes
        animated_elements = []
        current_time = 0
        
        for i, stroke in enumerate(self.strokes):
            if stroke['type'] == 'circle':
                # Animated circle
                element = f'''
                <circle cx="{stroke['cx']}" cy="{stroke['cy']}" r="{stroke['r']}"
                        fill="none" stroke="green" stroke-width="{STROKE_WIDTH}"
                        stroke-dasharray="{2 * math.pi * stroke['r']}"
                        stroke-dashoffset="{2 * math.pi * stroke['r']}"
                        opacity="0">
                    <animate attributeName="opacity" values="0;1" dur="0.1s" begin="{current_time}s" fill="freeze"/>
                    <animate attributeName="stroke-dashoffset" values="{2 * math.pi * stroke['r']};0" 
                             dur="{stroke['duration']}s" begin="{current_time}s" fill="freeze"/>
                </circle>'''
            else:
                # Animated path
                # Calculate path length for dash animation (approximation)
                path_length = len(stroke['data']) * 2  # Rough approximation
                element = f'''
                <path d="{stroke['data']}" fill="none" stroke="green" stroke-width="{STROKE_WIDTH}"
                      stroke-dasharray="{path_length}" stroke-dashoffset="{path_length}"
                      opacity="0" stroke-linecap="round" stroke-linejoin="round">
                    <animate attributeName="opacity" values="0;1" dur="0.1s" begin="{current_time}s" fill="freeze"/>
                    <animate attributeName="stroke-dashoffset" values="{path_length};0" 
                             dur="{stroke['duration']}s" begin="{current_time}s" fill="freeze"/>
                </path>'''
            
            animated_elements.append(element)
            current_time += stroke['duration'] + self.stroke_delay
        
        # Add a drawing cursor/pen that follows the drawing
        cursor = f'''
        <circle cx="-100" cy="-100" r="3" fill="red" opacity="0.7">
            <animate attributeName="opacity" values="0;0.7;0.7;0" dur="{total_duration}s" fill="freeze"/>
        </circle>'''
        
        svg_content = f'''
        <svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" 
             viewBox="{viewbox_x} {viewbox_y} {viewbox_width} {viewbox_height}"
             xmlns="http://www.w3.org/2000/svg">
            <title>{title}</title>
            <rect width="100%" height="100%" fill="white" stroke="lightgray" stroke-width="1"/>
            
            <!-- Grid lines for reference -->
            <defs>
                <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f0f0f0" stroke-width="0.5"/>
                </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" opacity="0.3"/>
            
            <!-- Animated strokes -->
            {''.join(animated_elements)}
            
            <!-- Title -->
            <text x="0" y="{viewbox_y + 20}" text-anchor="middle" font-family="Arial, sans-serif" 
                  font-size="12" fill="darkgreen">{title}</text>
        </svg>
        '''
        return svg_content

# Global drawer instance
drawer = AnimatedSVGDrawer()

# ==============================
# Base Drawing Functions
# ==============================

def draw_base_structure():
    """Draw the basic structure common to all characters."""
    drawer.clear()
    
    # Left vertical line
    drawer.penup()
    drawer.goto(LEFT_X, 0)
    drawer.pendown()
    drawer.forward(VERTICAL_HEIGHT, 90)
    
    # Left curve
    drawer.forward(CURVE_RADIUS, 45)
    left_curve_end = (drawer.current_x, -drawer.current_y)

    # Right vertical line
    drawer.penup()
    drawer.goto(RIGHT_X, 0)
    drawer.pendown()
    drawer.forward(VERTICAL_HEIGHT, 90)
    
    # Right curve
    drawer.forward(CURVE_RADIUS, 135)
    right_curve_end = (drawer.current_x, -drawer.current_y)

    # Horizontal connecting line
    drawer.penup()
    drawer.goto(left_curve_end[0], left_curve_end[1])
    drawer.pendown()
    drawer.goto(right_curve_end[0], right_curve_end[1])

    return left_curve_end, right_curve_end

def draw_base_with_middle_line(col_idx):
    """Draw base structure with an additional middle vertical line."""
    left_curve_end, right_curve_end = draw_base_structure()
    
    # Add middle vertical line
    mid_x = (left_curve_end[0] + right_curve_end[0]) / 2
    mid_y = left_curve_end[1]
    drawer.penup()
    drawer.goto(mid_x, -mid_y)
    drawer.pendown()
    
    if col_idx == 6:
        drawer.forward(EXTRA_HEIGHT, 135)  # Diagonal to left
    else:
        drawer.forward(EXTRA_HEIGHT, 90)   # Straight up
    
    return left_curve_end, right_curve_end

# ==============================
# Character Modification Functions
# ==============================

def add_right_horizontal_line():
    """Add a small horizontal line extending right."""
    drawer.penup()
    drawer.goto(RIGHT_X, VERTICAL_HEIGHT/2)
    drawer.pendown()
    drawer.forward(SMALL_LINE_LENGTH, 0)

def add_right_bottom_line():
    """Add a small horizontal line extending right from bottom."""
    drawer.penup()
    drawer.goto(RIGHT_X, 0)
    drawer.pendown()
    drawer.forward(SMALL_LINE_LENGTH, 0)

def add_right_extension():
    """Add a vertical extension downward from bottom of right vertical."""
    drawer.penup()
    drawer.goto(RIGHT_X, 0)
    drawer.pendown()
    drawer.forward(EXTENSION_LENGTH, -90)

def add_circle():
    """Add a circle at the bottom right of the character."""
    drawer.penup()
    drawer.goto(RIGHT_X + CIRCLE_RADIUS, 0)
    drawer.pendown()
    drawer.circle(CIRCLE_RADIUS)

def add_left_horizontal_line():
    """Add a small horizontal line extending left."""
    drawer.penup()
    drawer.goto(LEFT_X, VERTICAL_HEIGHT/2)
    drawer.pendown()
    drawer.forward(SMALL_LINE_LENGTH, 180)

def add_left_extension():
    """Add a vertical extension downward from bottom of left vertical."""
    drawer.penup()
    drawer.goto(LEFT_X, 0)
    drawer.pendown()
    drawer.forward(EXTENSION_LENGTH, -90)

def add_top_horizontal_line():
    """Add a horizontal line above the main structure."""
    drawer.penup()
    drawer.goto(LEFT_X, VERTICAL_HEIGHT + TOP_GAP)
    drawer.pendown()
    drawer.goto(RIGHT_X, VERTICAL_HEIGHT + TOP_GAP)

# ==============================
# Character Drawing Functions
# ==============================

def draw_be(): draw_base_structure()
def draw_bu(): draw_base_structure(); add_right_horizontal_line()
def draw_bi(): draw_base_structure(); add_right_bottom_line()
def draw_ba(): draw_base_structure(); add_right_extension()
def draw_bee(): draw_base_structure(); add_circle()
def draw_bi2(): draw_base_structure(); add_left_horizontal_line()
def draw_bo(): draw_base_structure(); add_left_extension()

def draw_ve(): draw_base_structure(); add_top_horizontal_line()
def draw_vu(): draw_base_structure(); add_right_horizontal_line(); add_top_horizontal_line()
def draw_vi(): draw_base_structure(); add_right_bottom_line(); add_top_horizontal_line()
def draw_va(): draw_base_structure(); add_right_extension(); add_top_horizontal_line()
def draw_vee(): draw_base_structure(); add_top_horizontal_line(); add_circle()
def draw_vi2(): draw_base_structure(); add_left_horizontal_line(); add_top_horizontal_line()
def draw_vo(): draw_base_structure(); add_left_extension(); add_top_horizontal_line()

def draw_se(): draw_base_with_middle_line(1)
def draw_su(): draw_base_with_middle_line(2); add_right_horizontal_line()
def draw_si(): draw_base_with_middle_line(3); add_right_bottom_line()
def draw_sa(): draw_base_with_middle_line(4); add_right_extension()
def draw_see(): draw_base_with_middle_line(5); add_circle()
def draw_si2(): draw_base_with_middle_line(6); add_left_horizontal_line()
def draw_so(): draw_base_with_middle_line(7); add_left_extension()

def draw_she(): draw_base_with_middle_line(1); add_top_horizontal_line()
def draw_shu(): draw_base_with_middle_line(2); add_right_horizontal_line(); add_top_horizontal_line()
def draw_shi(): draw_base_with_middle_line(3); add_right_bottom_line(); add_top_horizontal_line()
def draw_sha(): draw_base_with_middle_line(4); add_right_extension(); add_top_horizontal_line()
def draw_shee(): draw_base_with_middle_line(5); add_top_horizontal_line(); add_circle()
def draw_shi2(): draw_base_with_middle_line(6); add_left_horizontal_line(); add_top_horizontal_line()
def draw_sho(): draw_base_with_middle_line(7); add_left_extension(); add_top_horizontal_line()

# ==============================
# Character Data
# ==============================

CHARACTER_FAMILIES = {
    "በ Family (Row 1)": {
        "characters": [
            ("በ (be)", draw_be),
            ("ቡ (bu)", draw_bu),
            ("ቢ (bi)", draw_bi),
            ("ባ (ba)", draw_ba),
            ("ቤ (bee)", draw_bee),
            ("ቢ (bi2)", draw_bi2),
            ("ቦ (bo)", draw_bo)
        ]
    },
    "ቨ Family (Row 2)": {
        "characters": [
            ("ቨ (ve)", draw_ve),
            ("ቩ (vu)", draw_vu),
            ("ቪ (vi)", draw_vi),
            ("ቫ (va)", draw_va),
            ("ቬ (vee)", draw_vee),
            ("ቭ (vi2)", draw_vi2),
            ("ቮ (vo)", draw_vo)
        ]
    },
    "ሰ Family (Row 3)": {
        "characters": [
            ("ሰ (se)", draw_se),
            ("ሱ (su)", draw_su),
            ("ሲ (si)", draw_si),
            ("ሳ (sa)", draw_sa),
            ("ሴ (see)", draw_see),
            ("ሲ (si2)", draw_si2),
            ("ሶ (so)", draw_so)
        ]
    },
    "ሸ Family (Row 4)": {
        "characters": [
            ("ሸ (she)", draw_she),
            ("ሹ (shu)", draw_shu),
            ("ሺ (shi)", draw_shi),
            ("ሻ (sha)", draw_sha),
            ("ሼ (shee)", draw_shee),
            ("ሽ (shi2)", draw_shi2),
            ("ሾ (sho)", draw_sho)
        ]
    }
}

# ==============================
# Streamlit App
# ==============================

def main():
    st.set_page_config(
        page_title="Ethiopian Amharic Characters - Animated",
        page_icon="🇪🇹",
        layout="wide"
    )
    
    st.title("🇪🇹 Ethiopian Amharic Characters - Hand Drawing Animation")
    st.markdown("---")
    
    # Sidebar for options
    st.sidebar.title("Animation Options")
    view_mode = st.sidebar.radio(
        "View Mode:",
        ["Individual Characters", "Family Animations", "Full Sequence"]
    )
    
    # Animation speed control
    speed = st.sidebar.slider("Animation Speed", 0.5, 3.0, 1.0, 0.1)
    drawer.stroke_delay = 0.5 / speed
    
    if view_mode == "Individual Characters":
        show_individual_characters()
    elif view_mode == "Family Animations":
        show_family_animations()
    else:
        show_full_sequence()

def show_individual_characters():
    """Display individual character animation interface."""
    st.subheader("🎨 Individual Character Animation")
    
    # Family selection
    family_name = st.selectbox("Select Character Family:", list(CHARACTER_FAMILIES.keys()))
    
    # Character selection within family
    characters = CHARACTER_FAMILIES[family_name]["characters"]
    character_names = [char[0] for char in characters]
    selected_char = st.selectbox("Select Character:", character_names)
    
    # Animation controls
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("🎬 Animate Character", type="primary"):
            st.session_state.animate_single = True
        
        if st.button("🔄 Reset"):
            st.session_state.animate_single = False
    
    with col2:
        # Find and animate the selected character
        for name, draw_func in characters:
            if name == selected_char:
                if st.session_state.get('animate_single', False):
                    st.markdown(f"### ✍️ Drawing: {name}")
                    draw_func()
                    animated_svg = drawer.get_animated_svg(name)
                    st.markdown(
                        f'<div style="text-align: center; margin: 20px;">{animated_svg}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(f"### Preview: {name}")
                    st.markdown("*Click 'Animate Character' to see the hand-drawing animation*")
                break
    
    # Show character information
    with st.expander("📚 Character Information"):
        st.write(f"**Family:** {family_name}")
        st.write(f"**Character:** {selected_char}")
        st.write("This character is part of the Ethiopian Amharic script. "
                "The animation shows how the character would be hand-drawn stroke by stroke.")

def show_family_animations():
    """Display family-wise animations."""
    st.subheader("👨‍👩‍👧‍👦 Character Family Animations")
    
    family_name = st.selectbox("Select Family:", list(CHARACTER_FAMILIES.keys()))
    
    if st.button(f"🎬 Animate All {family_name}", type="primary"):
        characters = CHARACTER_FAMILIES[family_name]["characters"]
        
        st.markdown(f"### ✍️ Drawing all characters in {family_name}")
        
        # Create columns for side-by-side display
        cols = st.columns(4)
        
        for idx, (name, draw_func) in enumerate(characters):
            with cols[idx % 4]:
                draw_func()
                animated_svg = drawer.get_animated_svg(name)
                st.markdown(
                    f'<div style="text-align: center; margin: 5px;">'
                    f'{animated_svg}'
                    f'</div>',
                    unsafe_allow_html=True
                )

def show_full_sequence():
    """Display full sequence animation."""
    st.subheader("🎭 Complete Character Sequence Animation")
    st.write("Watch all 28 Amharic characters being drawn in sequence!")
    
    if st.button("🎬 Start Full Animation Sequence", type="primary"):
        st.markdown("### ✍️ Drawing All Amharic Characters...")
        
        # Create animation container
        animation_container = st.container()
        progress_bar = st.progress(0)
        
        total_families = len(CHARACTER_FAMILIES)
        current_family = 0
        
        for family_name, family_data in CHARACTER_FAMILIES.items():
            with animation_container:
                st.markdown(f"#### Now Drawing: {family_name}")
                
                characters = family_data["characters"]
                family_cols = st.columns(len(characters))
                
                for idx, (name, draw_func) in enumerate(characters):
                    with family_cols[idx]:
                        draw_func()
                        animated_svg = drawer.get_animated_svg(name)
                        st.markdown(
                            f'<div style="text-align: center; margin: 2px;">'
                            f'{animated_svg}'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                
                current_family += 1
                progress_bar.progress(current_family / total_families)
                
                # Add separator
                if current_family < total_families:
                    st.markdown("---")
        
        st.success("🎉 Animation sequence completed!")
        st.balloons()

if __name__ == "__main__":
    main()