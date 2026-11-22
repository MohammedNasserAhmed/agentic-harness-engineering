
 // MODEL FUNCTION
export async function getBookById(bookId) {
  const response = await fetch(
    `https://openlibrary.org/works/${bookId}.json`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch book");
  }

  return response.json();
}


// TODO(ai)
// Refactor this function to follow the same style as the model function.
export function getAuthorById(authorId) {
  return fetch("https://openlibrary.org/authors/" + authorId + ".json")
    .then(function(response) {
      return response.json();
    })
    .then(function(author) {
      return author;
    });
}
