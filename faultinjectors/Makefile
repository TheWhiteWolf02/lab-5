FAULTINJECTORS = fi_read_EINTR.so fi_read_EIO.so \
		 fi_write_ENOSPC.so fi_write_EIO.so \
		 fi_select_ENOMEM.so \
		 fi_malloc_ENOMEM.so

all: $(FAULTINJECTORS)

%.so: %.c
	gcc $< -fPIC -shared -o $@ -ldl

clean:
	rm -f $(FAULTINJECTORS)
