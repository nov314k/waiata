import ezdxf
import yaml

with open('1_change_settings_first.yaml', 'r') as stream:
	try:
		file = yaml.load(stream)
	except yaml.YAMLError as ex:
		print(ex)

dwg = ezdxf.new(file['settings']['dwg_standard'])msp = dwg.modelspace()
value_x = file['settings']['value_x']
value_y = file['settings']['value_y']
origin_x = file['settings']['origin_x']origin_y = file['settings']['origin_y']frame_width = file['settings']['frame_width']tick_spacing = file['settings']['tick_spacing']frame_height = file['settings']['frame_height']
text_alignment = file['settings']['text_alignment']save_as_filename = file['settings']['save_as_filename']first_standard_value = file['settings']['first_standard_value']
text_height = file['settings']['text_height']text_height = text_height * max(frame_width, frame_height) / 100digit_width_ratio = file['settings']['digit_width_ratio']offset_x = (digit_width_ratio / 2) * text_height / 100
offset_y = 2 * offset_x
tick_half_size = file['settings']['tick_half_size']tick_half_size = tick_half_size * max(frame_width, frame_height) / 100
msp.add_line((origin_x, origin_y), (origin_x + frame_width, origin_y))msp.add_line((origin_x + frame_width, origin_y), (origin_x + frame_width, origin_y + frame_height))msp.add_line((origin_x + frame_width, origin_y + frame_height), (origin_x, origin_y + frame_height))msp.add_line((origin_x, origin_y + frame_height), (origin_x, origin_y))
x_text_3 = value_x % 1000
x_text_2 = int(value_x / 1000) % 1000
x_text_1 = int(value_x / 1000 / 1000) % 1000
attribs = {'height': text_height} # , 'color': 1

msp.add_text(x_text_1, dxfattribs = attribs).set_pos(
	(origin_x - offset_x, origin_y - offset_y),
	align = text_alignment)
msp.add_text(x_text_2, dxfattribs = attribs).set_pos(
	(origin_x - offset_x, origin_y - 2*offset_y - text_height),
	align = text_alignment)
msp.add_text(x_text_3, dxfattribs = attribs).set_pos(
	(origin_x - offset_x, origin_y - 3*offset_y - 2*text_height),
	align = text_alignment)

current_position = origin_x + (first_standard_value - x_text_3)
while current_position < origin_x + frame_width:
	msp.add_line((current_position, origin_y - tick_half_size),
		(current_position, origin_y + tick_half_size))
	msp.add_text(x_text_3 + current_position - origin_x, dxfattribs = attribs).set_pos(
		(current_position - offset_x, origin_y - 3*offset_y - 2*text_height),
		align = text_alignment)
	current_position += tick_spacing

y_text_3 = value_y % 1000
y_text_2 = int(value_y / 1000) % 1000
y_text_1 = int(value_y / 1000 / 1000) % 1000

msp.add_text(y_text_1, dxfattribs = attribs).set_pos(
	(origin_x + frame_width + 4*offset_x, origin_y + offset_y),
	align = text_alignment)
msp.add_text(y_text_2, dxfattribs = attribs).set_pos(
	(origin_x + frame_width + 4*offset_x, origin_y - text_height),
	align = text_alignment)
msp.add_text(y_text_3, dxfattribs = attribs).set_pos(
	(origin_x + frame_width + 4*offset_x, origin_y - 1*offset_y - 2*text_height),
	align = text_alignment)

current_position = origin_y + (first_standard_value - y_text_3)
while current_position < origin_y + frame_height:
	msp.add_line(
		(origin_x + frame_width - tick_half_size, current_position),
		(origin_x + frame_width + tick_half_size, current_position))
	msp.add_text(y_text_3 + current_position - origin_y, dxfattribs = attribs).set_pos(
		(origin_x	 + frame_width + 4*offset_x, current_position + offset_y),
		align = text_alignment)
	current_position += tick_spacing

dwg.saveas(save_as_filename)