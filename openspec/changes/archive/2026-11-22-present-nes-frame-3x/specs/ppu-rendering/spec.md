# PPU Rendering

## Purpose

Produce native-size NES frames from PPU memory and registers for use by the host display.

## ADDED Requirements

### Requirement: Draw the backdrop color

The PPU SHALL produce a complete 256 × 240 RGB frame. Pixels with no visible background or sprite contribution
SHALL use the color at palette address $3F00.

#### Scenario: Display the first color from an emulated program

- **WHEN** a synthetic CPU program sets $3F00 through $2006 and $2007 with both layers disabled
- **THEN** every pixel of the next rendered frame has the RGB value for the written NES color

### Requirement: Draw background tiles and attributes

The PPU SHALL take tile numbers from the selected nametable and decode their two CHR bitplanes from the background
pattern table selected by $2000 bit 4. Each 16 × 16 region SHALL use the subpalette selected by its attribute bits.
Pattern index zero SHALL allow the backdrop or a sprite to show through.

#### Scenario: Render distinguishable pattern and attribute regions

- **WHEN** a nametable selects an asymmetric tile and adjacent attribute quadrants select different palettes
- **THEN** the pattern appears at the tile's position with the expected colors in each quadrant
- **AND** selecting the other background pattern table changes the pattern data used for the same tile number

### Requirement: Scroll the background at frame boundaries

The renderer SHALL start each visible frame with its initial nametable selection and scroll position. For
ordinary scroll offsets, crossing a 256-pixel horizontal or 240-pixel vertical boundary SHALL select the
adjacent logical nametable using the cartridge's mirroring.

#### Scenario: Cross both nametable boundaries

- **WHEN** nonzero horizontal and vertical scroll offsets expose adjacent logical nametables
- **THEN** pixels on either side of each boundary have the colors sourced from the corresponding nametable

### Requirement: Apply horizontal scroll changes within the visible frame

During the visible period, the first write of a $2005 pair SHALL update horizontal scroll and $2000 bit 0
SHALL update the horizontal nametable selection from the next scanline. Earlier lines SHALL retain the
previous horizontal settings. The frame's vertical origin SHALL remain the one selected at its start.

#### Scenario: Change the playfield origin after a stationary panel

- **WHEN** a synthetic program changes horizontal scroll and nametable selection during a visible scanline
- **THEN** lines through that scanline use the initial horizontal settings
- **AND** the subsequent lines use the new horizontal settings in the same published frame

### Requirement: Draw sprites from OAM and CHR

The PPU SHALL read sprite position, tile, flips, and subpalette from OAM. The top appears at OAM Y plus one.
In 8 × 8 mode $2000 bit 3 selects the pattern table. In 8 × 16 mode the tile number's low bit selects the table,
and the remaining bits select the even tile followed by the next tile. Pattern index zero SHALL be transparent.

#### Scenario: Render both sprite sizes

- **WHEN** OAM selects an asymmetric sprite of each supported size with distinct tile halves
- **THEN** each sprite has the selected size, position, CHR pattern, and sprite colors
- **AND** horizontal and vertical flips reverse the pixels along the corresponding axes

### Requirement: Resolve overlapping background and sprite pixels

At a sprite overlap, the first nontransparent pixel in OAM order SHALL determine the sprite candidate.
The candidate's priority bit SHALL place it behind an opaque background pixel when set. A transparent
background pixel SHALL allow the candidate to show.

#### Scenario: Compose two sprites and a background

- **WHEN** two ordered sprites overlap opaque and transparent background pixels
- **THEN** the first opaque sprite pixel is the candidate
- **AND** its priority bit decides whether the opaque background pixel covers it

### Requirement: Apply display layer and left-edge masks

The PPU SHALL independently enable the background and sprite layers through $2001 bits 3 and 4. Bits 1 and 2
SHALL independently permit their respective layers in the first eight columns of the frame.

#### Scenario: Switch among layer combinations

- **WHEN** the same scene is rendered with both layers disabled, only background, only sprites, and both enabled
- **THEN** the four frames contain the corresponding backdrop or layers
- **AND** each left-edge mask excludes only its corresponding layer in columns 0 through 7

### Requirement: Apply grayscale and color emphasis

When $2001 bit 0 is set, the renderer SHALL mask each palette color code with $30 before converting it to RGB.
Bits 5 through 7 SHALL apply the documented RGB approximation of red, green, and blue emphasis for the first
NTSC timing profile.

#### Scenario: Render one palette color with changed color controls

- **WHEN** a color whose code changes under the grayscale mask is displayed with grayscale enabled
- **THEN** the RGB value matches the masked code
- **AND** an emphasis bit attenuates the other two channels of a color with nonzero values in all three channels
