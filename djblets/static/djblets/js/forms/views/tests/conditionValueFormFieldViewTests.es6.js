suite('djblets/forms/views/ConditionValueFormFieldView', () => {
    function createValueField(html) {
        const view = new Djblets.Forms.ConditionValueFormFieldView({
            model: new Djblets.Forms.ConditionValueField({
                fieldName: 'my-field',
                fieldHTML: html
            })
        });
        view.render();

        return view;
    }

    it('Rendering', () => {
        const view = createValueField('<input type="text" />');

        expect(view.$input[0].tagName).toBe('INPUT');
        expect(view.$input.attr('type')).toBe('text');
        expect(view.$input.attr('name')).toBe('my-field');
    });

    describe('Methods', () => {
        describe('getValue', () => {
            it('<input>', () => {
                const view = createValueField(
                    '<input type="text" value="abc123" />');

                expect(view.getValue()).toBe('abc123');
            });

            it('<select>', () => {
                const view = createValueField([
                    '<select>',
                    '<option value="1">One</option>',
                    '<option value="2" selected="selected">Two</option>',
                    '</select>'
                ].join(''));

                expect(view.getValue()).toBe('2');
            });

            it('<textarea>', () => {
                const view = createValueField('<textarea></textarea>');

                view.setValue('abc123');

                expect(view.$input.val()).toBe('abc123');
            });
        });

        describe('setValue', () => {
            it('<input>', () => {
                const view = createValueField('<input type="text" />');

                view.setValue('abc123');

                expect(view.$input.val()).toBe('abc123');
            });

            it('<select>', () => {
                const view = createValueField([
                    '<select>',
                    '<option value="1">One</option>',
                    '<option value="2">Two</option>',
                    '</select>'
                ].join(''));

                view.setValue('2');

                expect(view.$input.val()).toBe('2');
            });

            it('<textarea>', () => {
                const view = createValueField('<textarea></textarea>');

                view.setValue('abc123');

                expect(view.$input.val()).toBe('abc123');
            });
        });
    });
});