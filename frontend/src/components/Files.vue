<template>
  <div class="flex flex-col items-center p-4 w-full relative">
    <div class="flex flex-row mb-32">
      <b-field label="Asynchrone" class="absolute left-4 w-4/12 flex flex-col mt-10">
        <b-radio-button
          v-model="asyncRule"
          native-value="0"
          class="async-celery-btn">
          Asynchrone Celery
        </b-radio-button>

        <b-radio-button v-model="asyncRule"
          native-value="1"
          class="async-q-btn">
          Asynchrone Q cluster
        </b-radio-button>

        <b-radio-button v-model="asyncRule"
          native-value="2"
          class="sync-btn">
          Synchrone
        </b-radio-button>

        <b-radio-button v-model="asyncRule"
          native-value="3"
          class="both-sync-btn">
          Asynchrone Django Q - Celery
        </b-radio-button>
      </b-field>
      <div class="text-4xl font-thin font-display">Liste des fichiers</div>
      <div class="absolute right-4 w-4/12 flex">
        <div class="flex flex-col">
          <div class="flex flex-row">
            <div
              class="
                flex
                px-4
                py-2
                text-lg text-white
                font-thin
                justify-center
                items-center
                bg-gradient-to-r
                from-green-500
                to-blue-500
                rounded
                mr-8
                cursor-pointer
                transition-all
                duration-500
                transform
                hover:scale-110
                text-center
                h-12
              "
              @click="retrieveFiles"
            >
              Récupérer
            </div>
            <div
              class="
                flex
                px-4
                py-2
                text-lg text-white
                font-thin
                justify-center
                items-center
                bg-gradient-to-r
                from-blue-500
                to-purple-500
                rounded
                cursor-pointer
                transition-all
                duration-500
                transform
                hover:scale-110
                text-center
                h-12
              "
              @click="generateNewOnes(false)"
            >
              Générer des nouveaux
            </div>
            <div class="flex flex-col ml-8">
              <div
                class="
                  flex
                  px-4
                  py-2
                  text-lg text-white
                  font-thin
                  justify-center
                  items-center
                  bg-gradient-to-r
                  from-purple-500
                  to-pink-500
                  rounded
                  cursor-pointer
                  transition-all
                  duration-500
                  transform
                  hover:scale-110
                  text-center
                  mb-2
                  h-12
                "
                @click="generateNewOnes(true)"
              >
                Simuler multiple génération
              </div>
            </div>
          </div>
          <div class="flex flex-row w-full justify-between items-center">
            <b-field class="mr-4" label="Quantité">
              <b-input v-model="quantity"></b-input>
            </b-field>
          </div>
        </div>
      </div>
    </div>
    <p class="text-black font-light text-md">Temps global : {{ timeGlobal / 1000 }} secondes </p>
    <b-table
      class="w-full mt-4 max-h-80 overflow-y-auto overflow-x-hidden"
      :data="localFiles"
      :per-page="perPage"
      :current-page.sync="currentPage"
      paginated
      :loading="isLoading"
    >
      <b-table-column
        v-slot="props"
        label="Nom du fichier"
        field="filename"
        class="is-narrow"
      >
        {{ props.row.filename }}
      </b-table-column>

      <b-table-column v-slot="props" field="file" label="Chemin du fichier">
        {{ props.row.file }}
      </b-table-column>

      <b-table-column v-slot="props" field="file" label="Téléchargement">
        <a
          class="flex justify-center items-center"
          :href="props.row.file"
          download
        >
          <b-icon class="text-green-700" icon="file-download"></b-icon>
        </a>
      </b-table-column>
      <template slot="empty" class="flex justify-center items-center">
        <section class="text-xl font-thin">Aucun fichiers.</section>
      </template>
    </b-table>

    <div
      class="
        flex
        px-4
        py-2
        text-lg text-white
        font-thin
        bg-gradient-to-r
        from-red-500
        to-red-800
        rounded
        cursor-pointer
        transition-all
        duration-500
        transform
        hover:scale-110
        mt-6
      "
      @click="deleteAll"
    >
      Supprimer
    </div>
    <div class="flex flex-row mt-10 w-full justify-around mx-16">
      <div class="flex flex-col items-center w-full mr-4">
        <div class="flex flex-row items-center">
          <p class="text-xl text-black">File d'attente <b>Django Q</b></p>
          <div
            class="
              flex
              py-2
              px-2
              font-thin
              bg-gradient-to-r
              from-red-500
              to-red-800
              rounded
              cursor-pointer
              transition-all
              duration-500
              transform
              hover:scale-110
              ml-2
            "
            @click="taskQueue(false)"
          >
            <b-icon class="text-white text-lg" icon="refresh"></b-icon>
          </div>
        </div>
        <p class="text-black font-light text-md">Temps : {{ timeDjangoQ / 1000 }} secondes </p>
        <b-table
          class="w-full mt-4"
          :data="localDjangoQTaskQueue"
          :per-page="perPage"
          :current-page.sync="djangoQCurrentPage"
          paginated
        >
          <b-table-column
            v-slot="props"
            label="Id"
            field="id"
            class="is-narrow"
          >
            {{ props.row.id }}
          </b-table-column>
          <template slot="empty" class="flex justify-center items-center">
            <section class="text-xl font-thin">File d'attente vide.</section>
          </template>
        </b-table>
      </div>
      <div class="flex flex-col items-center w-full ml-4">
        <div class="flex flex-row items-center">
          <p class="text-xl text-black">File d'attente <b>Celery</b></p>
          <div
            class="
              flex
              py-2
              px-2
              font-thin
              bg-gradient-to-r
              from-red-500
              to-red-800
              rounded
              cursor-pointer
              transition-all
              duration-500
              transform
              hover:scale-110
              ml-2
            "
            @click="taskQueue(false)"
          >
            <b-icon class="text-white text-lg" icon="refresh"></b-icon>
          </div>
        </div>
        <p class="text-black font-light text-lg">Nombre de process actifs : {{ localCeleryActiveWorkers }} </p>
        <p class="text-black font-light text-md">Temps : {{ timeCelery / 1000 }} secondes </p>
        <b-table
          class="w-full mt-4"
          :data="localCeleryTaskQueue"
          :per-page="perPage"
          :current-page.sync="celeryCurrentPage"
          paginated
        >
          <b-table-column
            v-slot="props"
            label="Id"
            field="id"
            class="is-narrow"
          >
            {{ props.row.id }}
          </b-table-column>

          <template slot="empty" class="flex justify-center items-center">
            <section class="text-xl font-thin">File d'attente vide.</section>
          </template>
        </b-table>
      </div>
    </div>
  </div>
</template>

<script>
import Files from "@/api/index";

export default {
  name: "Files",
  data() {
    return {
      headers: [
        { text: "Nom du fichier", value: "filename" },
        { text: "Chemin du fichier", value: "file" },
        { text: "Téléchargement", value: "" },
      ],
      files: [],
      djangoQTaskQueue: [],
      celeryTaskQueue: [],
      isLoading: false,
      currentPage: 1,
      perPage: 10,
      asyncRule: "2",
      quantity: 5,
      djangoQCurrentPage: 1,
      celeryCurrentPage: 1,
      celeryActiveWorkers: 0,
      subProcess: 2,
      start: 0,
      timeCelery: 0,
      timeDjangoQ: 0,
      timeGlobal: 0
    };
  },
  computed: {
    localFiles () {
      return this.files
    },
    localDjangoQTaskQueue() {
      return this.djangoQTaskQueue
    },
    localCeleryTaskQueue() {
      return this.celeryTaskQueue
    },
    localCeleryActiveWorkers() {
      return this.celeryActiveWorkers
    }
  },
  async created() {
    if (!this.files.length) this.files = await this.getFiles();
  },
  methods: {
    getFiles() {
      return new Promise((resolve, reject) => {
        Files.retrieve()
          .then((response) => {
            resolve(response.data);
          })
          .catch((error) => {
            console.log(error);
            reject();
          });
      });
    },
    generateNewOnes(multiple = false) {
      this.start = new Date().getTime();
      this.isLoading = true;
      Files.generateNewOnes(this.asyncRule, multiple, this.quantity)
        .then(response => {
          this.$buefy.snackbar.open({
            duration: 5000,
            message: "Génération de nouveaux fichiers en cours !",
          });
          if (this.asyncRule === "2") {
            response.data.forEach(file => {
              file.file = `http://localhost:8000${file.file}`
            })
            this.files = response.data
            var endGlobal = new Date().getTime();
            this.timeGlobal = endGlobal - this.start
          }
        })
        .catch((error) => {
          console.log(error);
        })
        .finally(() => {
          this.isLoading = false;
          if (["0", "1", "3"].includes(this.asyncRule)) this.taskQueue(true)
        });
    },
    async retrieveFiles() {
      this.files = await this.getFiles();
    },
    deleteAll() {
      Files.deleteAll()
        .then(() => {
          this.$buefy.snackbar.open({
            duration: 5000,
            message: "Suppression de tous les fichiers !",
          });
          this.files = [];
          this.timeGlobal = 0;
          this.timeCelery = 0;
          this.timeDjangoQ = 0
        })
        .catch((error) => {
          console.log(error);
        });
    },
    taskQueue(with_loop = false) {
      Files.retrieveCeleryInfo()
        .then(response => {
          this.celeryTaskQueue = response.data.celery
          this.djangoQTaskQueue = response.data.django_q
          this.celeryActiveWorkers = response.data.celery_active_workers
          this.getFiles().then(result => {
            this.files = result
            if (with_loop && (response.data.celery_continue || response.data.django_q_continue)) {
              this.taskQueue(true)
              if (this.asyncRule == "3" && !response.data.django_q_continue && !this.timeDjangoQ) {
                var endDjango = new Date().getTime();
                this.timeDjangoQ = endDjango - this.start;
              }
              if (this.asyncRule == "3" && !response.data.celery_continue && !this.timeCelery) {
                var endCelery = new Date().getTime();
                this.timeCelery = endCelery - this.start;
              }
            } else {
              this.celeryActiveWorkers = 0
              this.celeryTaskQueue = []
              if (["1", "3"].includes(this.asyncRule) && !this.timeDjangoQ) {
                var endDjangoTwo = new Date().getTime();
                this.timeDjangoQ = endDjangoTwo - this.start;
              }
              if (["0", "3"].includes(this.asyncRule) && !this.timeCelery) {
                var endCeleryTwo = new Date().getTime();
                this.timeCelery = endCeleryTwo - this.start;
              }
              var endGlobal = new Date().getTime();
              this.timeGlobal = endGlobal - this.start
            }
          })
        })
        .catch((error) => {
          console.log(error);
        });
    }
  },
};
</script>

<style lang="scss">
.async-celery-btn {
  .b-radio {
    @apply border-white border-r-0 text-lg bg-gradient-to-r from-yellow-500 to-green-500 text-white font-thin cursor-pointer transition-all duration-500 transform hover:scale-110 hover:text-white hover:border-white
  }

  .is-selected {
    @apply bg-gradient-to-r from-red-500 to-yellow-500 scale-110
  }
}

.async-q-btn {
  .b-radio {
    @apply border-white border-r-0 border-l-0 text-lg bg-gradient-to-r from-green-500 to-blue-500 text-white font-thin cursor-pointer transition-all duration-500 transform hover:scale-110 hover:text-white hover:border-white
  }

  .is-selected {
    @apply bg-gradient-to-r from-red-500 to-yellow-500 scale-110
  }
}

.sync-btn {
  .b-radio {
    @apply border-white border-l-0 text-lg bg-gradient-to-r from-blue-500 to-purple-500 text-white font-thin cursor-pointer transition-all duration-500 transform hover:scale-110 hover:text-white hover:border-white
  }

  .is-selected {
    @apply bg-gradient-to-r from-red-500 to-yellow-500 scale-110
  }
}

.both-sync-btn {
  .b-radio {
    @apply border-white border-l-0 text-lg bg-gradient-to-r from-purple-500 to-pink-500 text-white font-thin cursor-pointer transition-all duration-500 transform hover:scale-110 hover:text-white hover:border-white
  }

  .is-selected {
    @apply bg-gradient-to-r from-red-500 to-yellow-500 scale-110
  }
}

</style>
