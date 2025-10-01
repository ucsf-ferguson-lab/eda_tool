<template>
  <div class="dataset-explorer">
    <h1>Simple Dataset Explorer</h1>

    <div class="uploader">
      <input type="file" accept=".csv" @change="handleFileUpload" />
    </div>

    <div v-if="data.length > 0">
      <div class="tabs">
        <button
          :class="{ active: activeTab === 'preview' }"
          @click="activeTab = 'preview'"
        >
          Data Preview
        </button>
        <button
          :class="{ active: activeTab === 'summary' }"
          @click="activeTab = 'summary'"
        >
          Summary Statistics
        </button>
      </div>

      <!-- tab 1: data preview -->
      <div v-if="activeTab === 'preview'" class="tab-content">
        <h2>Data Preview</h2>
        <table>
          <thead>
            <tr>
              <th v-for="col in columns" :key="col">{{ col }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in paginatedData" :key="i">
              <td v-for="col in columns" :key="col">{{ row[col] }}</td>
            </tr>
          </tbody>
        </table>

        <!-- 1 page = 15 rows, allow jump to page -->
        <div class="pagination">
          <button :disabled="currentPage === 1" @click="currentPage--">
            Previous
          </button>
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="currentPage++">
            Next
          </button>

          <div class="jump">
            <label for="jumpPage">Jump to page:</label>
            <input
              id="jumpPage"
              type="number"
              v-model.number="jumpTo"
              :min="1"
              :max="totalPages"
              @keyup.enter="goToPage"
            />
            <button @click="goToPage">Go</button>
          </div>
        </div>
      </div>

      <!-- tab 2: summary stats -->
      <div v-if="activeTab === 'summary'" class="tab-content">
        <h2>Summary Statistics</h2>
        <table>
          <thead>
            <tr>
              <th>Variable</th>
              <th>Unique</th>
              <th>Count</th>
              <th>Mean</th>
              <th>Std</th>
              <th>Min</th>
              <th>Max</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(stats, col) in summaryStats" :key="col">
              <td>{{ col }}</td>
              <td>{{ stats.unique }}</td>
              <td>{{ stats.count }}</td>
              <td>{{ stats.mean ?? "-" }}</td>
              <td>{{ stats.std ?? "-" }}</td>
              <td>{{ stats.min ?? "-" }}</td>
              <td>{{ stats.max ?? "-" }}</td>
            </tr>
          </tbody>
        </table>

        <h2>Variable Distribution</h2>
        <div>
          <label for="columnSelect">Select a variable:</label>
          <select id="columnSelect" v-model="selectedColumn">
            <option v-for="col in columns" :value="col" :key="col">
              {{ col }}
            </option>
          </select>
        </div>

        <canvas v-if="selectedColumn" ref="chartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, watch, nextTick, computed } from "vue";
import Papa from "papaparse";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

interface Stats {
  unique: number;
  count: number;
  mean?: number;
  std?: number;
  min?: number;
  max?: number;
}

export default defineComponent({
  name: "DatasetExplorer",
  setup() {
    const data = ref<any[]>([]);
    const columns = ref<string[]>([]);
    const activeTab = ref<"preview" | "summary">("preview");
    const summaryStats = reactive<Record<string, Stats>>({});
    const selectedColumn = ref<string>("");
    const chartCanvas = ref<HTMLCanvasElement | null>(null);
    let chart: Chart | null = null;

    //pagination state
    const currentPage = ref(1);
    const rowsPerPage = 15;
    const jumpTo = ref<number>(1);

    const totalPages = computed(() =>
      Math.ceil(data.value.length / rowsPerPage),
    );

    const paginatedData = computed(() => {
      const start = (currentPage.value - 1) * rowsPerPage;
      const end = start + rowsPerPage;
      return data.value.slice(start, end);
    });

    const goToPage = () => {
      if (!jumpTo.value) return;
      if (jumpTo.value < 1) {
        currentPage.value = 1;
      } else if (jumpTo.value > totalPages.value) {
        currentPage.value = totalPages.value;
      } else {
        currentPage.value = jumpTo.value;
      }
    };

    //reset pagination when dataset changes
    watch(data, () => {
      currentPage.value = 1;
      jumpTo.value = 1;
    });

    const handleFileUpload = (event: Event) => {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (!file) return;
      Papa.parse(file, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete(results: { data: any[]; meta: { fields: string[] } }) {
          data.value = results.data;
          columns.value = results.meta.fields || [];
          calculateStats();
        },
      });
    };

    const calculateStats = () => {
      Object.keys(summaryStats).forEach((k) => delete summaryStats[k]);

      columns.value.forEach((col) => {
        const values = data.value
          .map((row) => row[col])
          .filter((v) => v !== null && v !== undefined);
        const numericValues = values.filter(
          (v) => typeof v === "number",
        ) as number[];
        const stats: Stats = {
          unique: new Set(values).size,
          count: values.length,
        };
        if (numericValues.length > 0) {
          const mean =
            numericValues.reduce((a, b) => a + b, 0) / numericValues.length;
          const variance =
            numericValues.reduce((a, b) => a + (b - mean) ** 2, 0) /
            numericValues.length;
          stats.mean = mean;
          stats.std = Math.sqrt(variance);
          stats.min = Math.min(...numericValues);
          stats.max = Math.max(...numericValues);
        }
        summaryStats[col] = stats;
      });
    };

    const plotColumn = async () => {
      if (!chartCanvas.value || !selectedColumn.value) return;
      if (chart) chart.destroy();

      const values = data.value
        .map((row) => row[selectedColumn.value])
        .filter((v) => v !== null && v !== undefined);
      const isNumeric = values.every((v) => typeof v === "number");

      const ctx = chartCanvas.value.getContext("2d");
      if (!ctx) return;

      if (isNumeric) {
        chart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: values.map((_, i) => i.toString()),
            datasets: [
              {
                label: `Distribution of ${selectedColumn.value}`,
                data: values,
                backgroundColor: "rgba(54, 162, 235, 0.6)",
              },
            ],
          },
        });
      } else {
        const counts: Record<string, number> = {};
        values.forEach((v) => {
          counts[v] = (counts[v] || 0) + 1;
        });
        chart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: Object.keys(counts),
            datasets: [
              {
                label: `Value counts of ${selectedColumn.value}`,
                data: Object.values(counts),
                backgroundColor: "rgba(0, 0, 255, 1)",
              },
            ],
          },
        });
      }
    };

    watch(selectedColumn, async () => {
      await nextTick();
      plotColumn();
    });

    return {
      handleFileUpload,
      data,
      columns,
      activeTab,
      summaryStats,
      selectedColumn,
      chartCanvas,
      currentPage,
      totalPages,
      paginatedData,
      jumpTo,
      goToPage,
    };
  },
});
</script>

<style scoped>
.dataset-explorer {
  font-family: Arial, sans-serif;
  padding: 20px;
}

.uploader {
  margin-bottom: 20px;
}

.tabs button {
  margin-right: 10px;
  padding: 5px 10px;
  cursor: pointer;
}

.tabs .active {
  background-color: #007bff;
  color: white;
}

table {
  border-collapse: collapse;
  margin-top: 15px;
  width: 100%;
}
th,
td {
  border: 1px solid #ddd;
  padding: 8px;
}

.pagination {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.jump {
  display: flex;
  align-items: center;
  gap: 5px;
}
.jump input {
  width: 60px;
  padding: 3px;
}
</style>
