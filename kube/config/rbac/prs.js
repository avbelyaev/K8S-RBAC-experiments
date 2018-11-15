let out = JSON.parse(process.env.IN);
const fields = (process.env.FLD).split(".");
for (key in fields) {
    let field = fields[key];
    let array_field = field.split('[');
    if (array_field.length > 1) {
        let array_field_index = array_field[1].split(']')[0];
        let array_field_name = array_field[0];
        out = out[array_field_name][array_field_index];
    } else {
        out = out[field];
    }
}
console.log(out);

