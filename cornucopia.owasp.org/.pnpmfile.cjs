module.exports = {
	hooks: {
		readPackage(packageJson) {
			const cookieSpec = packageJson.dependencies?.cookie;
			if (cookieSpec && /^(<0\.7\.0|\^0\.|~0\.|0\.)/.test(cookieSpec)) {
				packageJson.dependencies.cookie = '0.7.2';
			}

			if (packageJson.name === 'then-request' && packageJson.dependencies?.qs) {
				packageJson.dependencies.qs = '6.15.2';
			}

			return packageJson;
		},
	},
};
