from user_assistant.notes.note_record import NoteRecord


note_titles = ["🤠 Author", "📝 Text", "🖇 Tags", "🎱 ID", "📅 Updated at", "📅 Created at"]


def get_notes_row(record: NoteRecord):
    return [
        record.author.value,
        record.text.value,
        ", ".join(record.str_tags),
        str(record.id),
        str(record.updated_at),
        str(record.created_at),
    ]
