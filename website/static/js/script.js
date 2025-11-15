function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ note: noteId })
    }).then((_res) => {
        window.location.href = "/";
    });
}