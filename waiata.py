import ezdxf
import yaml

def distance_to_first_standard_value(coord):
	limit = 100
	while (coord >= limit):
		limit += 100
	return limit - coord

with open('1_change_settings_first.yaml', 'r') as stream:
	try:
		file = yaml.load(stream)
	except yaml.YAMLError as ex:
		print(ex)

dwg = ezdxf.new(file['settings']['dwg_standard'])msp = dwg.modelspace()

value_x = file['settings']['value_x']
value_y = file['settings']['value_y']
origin_x = value_xorigin_y = value_ylayer_name = file['settings']['layer_name']frame_width = file['settings']['frame_width']tick_spacing = file['settings']['tick_spacing']frame_height = file['settings']['frame_height']
x_text_alignment = file['settings']['x_text_alignment']
y_text_alignment = file['settings']['y_text_alignment']save_as_filename = file['settings']['save_as_filename']

text_height = file['settings']['text_height']text_height = text_height * max(frame_width, frame_height) / 100digit_width_ratio = file['settings']['digit_width_ratio']offset_x = (digit_width_ratio) * text_height / 100
offset_y = offset_x
tick_half_size = file['settings']['tick_half_size']tick_half_size = tick_half_size * max(frame_width, frame_height) / 100
dwg.layers.new(name = layer_name, dxfattribs = {'color': 0})
line_attribs = {'layer': layer_name}
x_text_attribs = {'height': text_height, 'layer': layer_name, 'rotation': 90}
y_text_attribs = {'height': text_height, 'layer': layer_name}

msp.add_line(
	(origin_x, origin_y),
	(origin_x + frame_width, origin_y),
	dxfattribs = line_attribs)msp.add_line(
	(origin_x + frame_width, origin_y),
	(origin_x + frame_width, origin_y + frame_height),
	dxfattribs = line_attribs)msp.add_line(
	(origin_x + frame_width, origin_y + frame_height),
	(origin_x, origin_y + frame_height),
	dxfattribs = line_attribs)msp.add_line(
	(origin_x, origin_y + frame_height),
	(origin_x, origin_y),
	dxfattribs = line_attribs)
x_text_3 = value_x % 1000
x_text_2 = int(value_x / 1000) % 1000
x_text_1 = int(value_x / 1000 / 1000) % 1000

msp.add_text(x_text_3, dxfattribs = x_text_attribs).set_pos(
	(origin_x - offset_x, origin_y - 2*offset_y),
	align = x_text_alignment)
msp.add_text(x_text_2, dxfattribs = x_text_attribs).set_pos(
	(origin_x - 2*offset_x - text_height, origin_y - 2*offset_y),
	align = x_text_alignment)
msp.add_text(x_text_1, dxfattribs = x_text_attribs).set_pos(
	(origin_x - 3*offset_x - 2*text_height, origin_y - 2*offset_y),
	align = x_text_alignment)

current_position = origin_x + distance_to_first_standard_value(x_text_3)
while current_position < origin_x + frame_width:
	msp.add_line(
		(current_position, origin_y),
		(current_position, origin_y + tick_half_size),
		dxfattribs = line_attribs)
	msp.add_text(x_text_3 + current_position - origin_x, dxfattribs = x_text_attribs).set_pos(
		(current_position - offset_x, origin_y - 2*offset_y),
		align = x_text_alignment)
	current_position += tick_spacing

y_text_3 = value_y % 1000
y_text_2 = int(value_y / 1000) % 1000
y_text_1 = int(value_y / 1000 / 1000) % 1000

msp.add_text(y_text_3, dxfattribs = y_text_attribs).set_pos(
	(origin_x + frame_width + 2*offset_x, origin_y + offset_y),
	align = y_text_alignment)
msp.add_text(y_text_2, dxfattribs = y_text_attribs).set_pos(
	(origin_x + frame_width + 2*offset_x, origin_y + 2*offset_y + text_height),
	align = y_text_alignment)
msp.add_text(y_text_1, dxfattribs = y_text_attribs).set_pos(
	(origin_x + frame_width + 2*offset_x, origin_y + 3*offset_y +	 2*text_height),
	align = y_text_alignment)

current_position = origin_y + distance_to_first_standard_value(y_text_3)
while current_position < origin_y + frame_height:
	msp.add_line(
		(origin_x + frame_width - tick_half_size, current_position),
		(origin_x + frame_width, current_position),
		dxfattribs = line_attribs)
	msp.add_text(y_text_3 + current_position - origin_y, dxfattribs = y_text_attribs).set_pos(
		(origin_x	 + frame_width + 2*offset_x, current_position + offset_y),
		align = y_text_alignment)
	current_position += tick_spacing

dwg.saveas(save_as_filename)