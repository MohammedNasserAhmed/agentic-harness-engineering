const bookForm = document.querySelector("#book-form");
const bookTitle = document.querySelector("#book-title");
const bookList = document.querySelector("#book-list");
const statusMessage = document.querySelector("#status");
const submitButton = bookForm.querySelector("button");

function showStatus(message, isError = false) {
  statusMessage.textContent = message;
  statusMessage.classList.toggle("error", isError);
}

function renderBooks(books) {
  bookList.replaceChildren();

  books.forEach((book) => {
    const item = document.createElement("li");
    item.textContent = `${book.id}. ${book.title}`;
    bookList.appendChild(item);
  });
}

async function loadBooks() {
  try {
    const response = await fetch("/api/books");
    if (!response.ok) {
      throw new Error("Could not load books");
    }

    const books = await response.json();
    renderBooks(books);
    showStatus(books.length ? `${books.length} book(s) in your library.` : "Your library is empty.");
  } catch (error) {
    showStatus(error.message, true);
  }
}

bookForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const title = bookTitle.value.trim();

  if (!title) {
    showStatus("Enter a book title first.", true);
    return;
  }

  submitButton.disabled = true;

  try {
    const response = await fetch("/api/books", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });

    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || "Could not add the book");
    }

    bookTitle.value = "";
    await loadBooks();
    bookTitle.focus();
  } catch (error) {
    showStatus(error.message, true);
  } finally {
    submitButton.disabled = false;
  }
});

loadBooks();
