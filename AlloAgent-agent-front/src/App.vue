<template>
	<v-app>
		<v-main>
				<router-view></router-view>
		</v-main>
	</v-app>
</template>

<script lang="ts">
	import { Component, Vue, Prop} from 'vue-property-decorator';

	@Component({
		name: 'App',
	})
	export default class App extends Vue {

	}
</script>
