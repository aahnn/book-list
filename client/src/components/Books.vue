<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>My Books</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal>Add Book</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <!--<button-->
                <!--scope = "col"-->
                <!--type="button"-->
                <!--@click="sortBooks('title')">-->
                <!--Title-->
              <!--</button>-->
              <!--<button-->
                <!--type="button"-->
                <!--@click="sortBooks('author')">-->
                <!--Author-->
              <!--</button>-->
              <!--<button-->
                <!--type="button"-->
                <!--@click="sortBooks('status')">-->
                <!--Status-->
              <!--</button>-->
              <!--<button-->
                <!--type="button"-->
                <!--@click="sortBooks('rating')">-->
                <!--Rating-->
              <!--</button>-->
              <th scope="col">
                <button
                  scope = "col"
                  type="button"
                  @click="sortBooks('title')">
                  Title
                </button>
              </th>
              <th scope="col">
                <button
                  scope = "col"
                  type="button"
                  @click="sortBooks('author')">
                  Author
                </button>
              </th>
              <th scope="col">
                <button
                  scope = "col"
                  type="button"
                  @click="sortBooks('status')">
                  Status
                </button>
              </th>
              <th scope="col">
                <button
                  scope = "col"
                  type="button"
                  @click="sortBooks('rating')">
                  Rating
                </button>
              </th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td><span>{{book.status}}</span></td>
              <td><span>{{book.rating}}</span></td>
              <td>
                <button
                        type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.book-update-modal
                        @click="editBook(book)">
                    Edit
                </button>
                <button
                        type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeleteBook(book)">
                    -
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addBookModal"
             id="book-modal"
             title="Add a new book"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addBookForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addBookForm.author"
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-rating-group"
                      label="Rating:"
                      label-for="form-rating-input">
            <b-form-input id="form-rating-input"
                          type="text"
                          v-model="addBookForm.rating"
                          placeholder="Enter rating out of 10">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="addBookForm.status" id="form-checks">
            <b-form-checkbox value="Finished">Finished</b-form-checkbox>
            <b-form-checkbox value="Want to read">Want to read</b-form-checkbox>
            <b-form-checkbox value="Reading">Reading</b-form-checkbox>
            <b-form-checkbox value="Dropped">Dropped</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editBookModal"
             id="book-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Author:"
                      label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="editForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-rating-edit-group"
                      label="Rating:"
                      label-for="form-rating-edit-input">
            <b-form-input id="form-rating-edit-input"
                          type="text"
                          v-model="editForm.rating"
                          placeholder="Enter rating out of 10">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-edit-group">
          <b-form-checkbox-group v-model="editForm.status" id="form-checks">
            <b-form-checkbox value="Finished">Finished</b-form-checkbox>
            <b-form-checkbox value="Want to read">Want to read</b-form-checkbox>
            <b-form-checkbox value="Reading">Reading</b-form-checkbox>
            <b-form-checkbox value="Dropped">Dropped</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      books: [],
      addBookForm: {
        title: '',
        author: '',
        status: [],
        rating: '',
      },
      editForm: {
        id: '',
        title: '',
        author: '',
        status: [],
        rating: '',
      },
    };
  },
  methods: {
    getBooks() {
      const path = 'http://localhost:5000/books';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    sortBooks(sortby) {
      const path = `http://localhost:5000/books/${sortby}`;
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addBook(payload) {
      const path = 'http://localhost:5000/books';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    editBook(book) {
      this.editForm = book;
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getBooks();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    initForm() {
      this.addBookForm.title = '';
      this.addBookForm.author = '';
      this.addBookForm.status = [];
      this.addBookForm.rating = '';
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.author = '';
      this.editForm.status = [];
      this.editForm.rating = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      const payload = {
        title: this.addBookForm.title,
        author: this.addBookForm.author,
        status: this.addBookForm.status[0],
        rating: this.addBookForm.rating,
      };
      this.addBook(payload);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      const payload = {
        title: this.editForm.title,
        author: this.editForm.author,
        status: this.editForm.status,
        rating: this.editForm.rating,
      };
      this.updateBook(payload, this.editForm.id);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      this.initForm();
      this.getBooks();
    },
    removeBook(bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.delete(path)
        .then(() => {
          this.getBooks();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onDeleteBook(book) {
      this.removeBook(book.id);
    },
  },
  created() {
    this.getBooks();
  },
};
</script>
