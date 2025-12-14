#include <stdio.h>
#include <sys/stat.h>
#include <stdint.h>
#include <unistd.h>

uint64_t t1,t2,t3,t4,t5,t6;

// 读取TSC计数器
static inline uint64_t rdtsc_lfence(void)
{
	uint32_t eax, edx;
	__asm__ __volatile__(
		"lfence\n\t"
		"rdtsc\n\t"
		"lfence"
		: "=a"(eax), "=d"(edx)
		:
		: "memory");
	return ((uint64_t)edx << 32) | eax;
}

/* 读取单个 sysfs 文件 */
static int read_sysfs_u64(const char *path, uint64_t *value)
{
	FILE *fp = fopen(path, "r");

	if (!fp) {
		return -1;
	}

	int ret = fscanf(fp, "%lu", value);
	fclose(fp);

	return (ret == 1) ? 0 : -1;
}

int main(void) {
	mode_t old_mask;
	int i;

	for (i = 0; i < 2; i++) {
		printf("wait %d seconds\n", i);
		sleep(1);
	}

	for (i = 0; i < 1000; i++) {
		t1 = rdtsc_lfence();
		old_mask = umask(0022);
		t6 = rdtsc_lfence();
	}

	sleep(1);

	read_sysfs_u64("/sys/kernel/fred/tsc_t1", &t2);
	read_sysfs_u64("/sys/kernel/fred/tsc_t2", &t3);
	read_sysfs_u64("/sys/kernel/fred/tsc_t3", &t4);
	read_sysfs_u64("/sys/kernel/fred/tsc_t4", &t5);

	printf("T1: %lu\n", t1);
	printf("T2: %lu\n", t2);
	//printf("T3: %lu\n", t3);
	//printf("T4: %lu\n", t4);
	printf("T5: %lu\n", t5);
	printf("T6: %lu\n", t6);

	printf("Total: %lu\n", t6-t1);
	printf(" u->k: %lu\n", t2-t1);
	printf(" k->k: %lu\n", t5-t2);
	printf(" k->u: %lu\n", t6-t5);

	return 0;
}
