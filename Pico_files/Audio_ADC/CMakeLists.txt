add_executable(adc)

# must match with executable name and source file names
target_sources(adc PRIVATE adc.c)

# must match with executable name
target_link_libraries(adc PRIVATE pico_stdlib pico_multicore pico_bootsel_via_double_reset hardware_pio hardware_dma hardware_adc hardware_irq)

# must match with executable name
pico_add_extra_outputs(adc)
