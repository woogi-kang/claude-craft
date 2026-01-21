import os

def create_context_window_svg(filename):
    """
    Generates a stacked bar chart for Context Window Usage.
    Data:
    - System Prompt: 2,000
    - History: 10,000
    - Tool Definitions: 5,000
    - Codebase: 80,000
    - Docs: 20,000
    - Remaining: 11,000
    Total: 128,000
    """
    
    data = [
        ("System Prompt", 2000, "#E5E7EB"),  # Gray-200
        ("Conversation History", 10000, "#D1D5DB"), # Gray-300
        ("Tool Definitions", 5000, "#9CA3AF"), # Gray-400
        ("Current Codebase", 80000, "#3B82F6"), # Blue-500 (Main intent)
        ("External Docs", 20000, "#60A5FA"), # Blue-400
        ("Free Space", 11000, "#10B981") # Emerald-500
    ]
    
    total = sum(item[1] for item in data)
    width = 800
    height = 200
    bar_height = 60
    bar_y = 70
    
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
    <rect width="{width}" height="{height}" fill="white"/>
    <text x="10" y="30" font-family="sans-serif" font-size="20" font-weight="bold" fill="#1F2937">Context Window Usage (~128k Token)</text>
    '''
    
    current_x = 50
    scale = (width - 100) / total
    
    # Draw bars
    for label, value, color in data:
        w = value * scale
        svg_content += f'<rect x="{current_x}" y="{bar_y}" width="{w}" height="{bar_height}" fill="{color}" stroke="white" stroke-width="1"/>'
        
        # Add legend/labels
        # If segment is too small, don't put text inside
        if w > 30:
            text_x = current_x + w/2
            # Alternate label positions to avoid overlap
            # For simplicity, just putting simple labels or legend below
            
        current_x += w

    # Draw Legend below
    legend_x = 50
    legend_y = 160
    for label, value, color in data:
        svg_content += f'''
        <g transform="translate({legend_x}, {legend_y})">
            <rect width="15" height="15" fill="{color}"/>
            <text x="20" y="12" font-family="sans-serif" font-size="12" fill="#4B5563">{label} ({value:,})</text>
        </g>
        '''
        legend_x += 160 # approximate spacing
        if legend_x > width - 100:
             legend_x = 50
             legend_y += 25

    svg_content += '</svg>'
    
    with open(filename, 'w') as f:
        f.write(svg_content)
    print(f"Generated {filename}")

def create_onion_architecture_svg(filename):
    """
    Generates Clean Architecture Onion Diagram.
    Concentric circles.
    """
    width = 600
    height = 600
    cx = width / 2
    cy = height / 2
    
    # Layers: (Label, Radius, Color, TextColor)
    # Outer to Inner
    layers = [
        ("Frameworks & Drivers", 280, "#DBEAFE", "#1E3A8A"), # Blue-100, Blue-900
        ("Interface Adapters", 210, "#D1FAE5", "#064E3B"),   # Green-100, Green-900
        ("Application Layer", 140, "#FCE7F3", "#831843"),    # Pink-100, Pink-900
        ("Domain Layer", 70, "#FEF3C7", "#78350F")           # Yellow-100, Yellow-900
    ]
    
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
    <rect width="{width}" height="{height}" fill="white"/>
    '''
    
    # Draw Circles
    for label, radius, fill, stroke in layers:
        svg_content += f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    
    # Draw Meta Text (Labels need to be placed carefully)
    # Usually labels are at the top of the ring
    
    # Frameworks
    svg_content += f'<text x="{cx}" y="{cy - 230}" text-anchor="middle" font-family="sans-serif" font-weight="bold" fill="#1E3A8A">Frameworks & Drivers</text>'
    svg_content += f'<text x="{cx}" y="{cy - 215}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#1E3A8A">(DB, UI, External Interfaces, Web)</text>'
    
    # Adapters
    svg_content += f'<text x="{cx}" y="{cy - 170}" text-anchor="middle" font-family="sans-serif" font-weight="bold" fill="#064E3B">Interface Adapters</text>'
    svg_content += f'<text x="{cx}" y="{cy - 155}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#064E3B">(Controllers, Gateways, Presenters)</text>'
    
    # Application
    svg_content += f'<text x="{cx}" y="{cy - 100}" text-anchor="middle" font-family="sans-serif" font-weight="bold" fill="#831843">Application Layer</text>'
    svg_content += f'<text x="{cx}" y="{cy - 85}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#831843">(Use Cases)</text>'

    # Domain
    svg_content += f'<text x="{cx}" y="{cy}" dy="5" text-anchor="middle" font-family="sans-serif" font-weight="bold" fill="#78350F">Domain Layer\n(Entities)</text>'
    
    # Arrow for dependency rule
    arrow_path = f"M {cx-280} {cy} L {cx-20} {cy}" 
    # Actually let's draw a separate arrow indicator on the side
    
    svg_content += f'''
    <g transform="translate(20, {height-50})">
        <text x="0" y="0" font-family="sans-serif" font-size="14" font-weight="bold">Dependency Rule:</text>
        <line x1="130" y1="-5" x2="200" y2="-5" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <text x="130" y="15" font-family="sans-serif" font-size="12">Outer → Inner</text>
    </g>
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <path d="M0,0 L0,6 L9,3 z" fill="black" />
        </marker>
    </defs>
    '''

    svg_content += '</svg>'

    with open(filename, 'w') as f:
        f.write(svg_content)
    print(f"Generated {filename}")

if __name__ == "__main__":
    output_dir = "work-blog/images"
    create_context_window_svg(os.path.join(output_dir, "context-token-usage.svg"))
    create_onion_architecture_svg(os.path.join(output_dir, "clean-architecture-onion.svg"))
